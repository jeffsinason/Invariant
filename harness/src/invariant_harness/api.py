from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from invariant_harness.benchmark import build_benchmark_report
from invariant_harness.case_registry import CASE_REGISTRY
from invariant_harness.models import DEFAULT_MODEL_NAMES, list_supported_models, load_model
from invariant_harness.result_store import (
    get_results_dir,
    save_benchmark_report,
    save_error_result,
)
from invariant_harness.runners.batch_runner import BatchRunner
from invariant_harness.runners.simple_runner import SimpleRunner
from invariant_harness.types import CaseResult

app = FastAPI(title="Invariant API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunCaseRequest(BaseModel):
    case_name: str
    provider: str | None = None
    model_name: str | None = None
    save: bool = True


class RunBenchmarkRequest(BaseModel):
    provider: str | None = None
    model_name: str | None = None
    case_names: list[str] = Field(default_factory=list)
    save: bool = True


def _case_result_to_payload(result: CaseResult, saved_path: str | None = None) -> dict[str, Any]:
    payload = result.to_dict()
    payload["saved_path"] = saved_path
    return payload


def _list_artifact_paths(prefix: str) -> list[Path]:
    results_dir = get_results_dir()
    return sorted(results_dir.glob(f"{prefix}*.json"), reverse=True)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/providers")
def list_providers() -> list[dict[str, str]]:
    return [
        {"provider": provider, "default_model": model_name}
        for provider, model_name in DEFAULT_MODEL_NAMES.items()
    ]


@app.get("/models")
def list_models(provider: str | None = None) -> list[dict[str, str | bool]]:
    try:
        return list_supported_models(provider=provider)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/cases")
def list_cases() -> list[str]:
    return sorted(CASE_REGISTRY.keys())


@app.post("/runs/case")
def run_case(request: RunCaseRequest) -> dict[str, Any]:
    try:
        model = load_model(provider=request.provider, model_name=request.model_name)
        runner = SimpleRunner(model=model)
        result, saved_path = runner.run(request.case_name, save=request.save)
        return {"result": _case_result_to_payload(result, saved_path)}
    except (RuntimeError, ValueError) as exc:
        selected_provider = request.provider or "mock"
        selected_model_name = (
            request.model_name or DEFAULT_MODEL_NAMES.get(selected_provider, "unknown-model")
        )
        saved_path = None
        if request.save:
            saved_path = str(
                save_error_result(
                    case_name=request.case_name,
                    provider=selected_provider,
                    model_name=selected_model_name,
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                )
            )

        raise HTTPException(
            status_code=400,
            detail={
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "saved_path": saved_path,
            },
        ) from exc


@app.post("/runs/benchmark")
def run_benchmark(request: RunBenchmarkRequest) -> dict[str, Any]:
    case_names = request.case_names or sorted(CASE_REGISTRY.keys())

    try:
        model = load_model(provider=request.provider, model_name=request.model_name)
        runner = BatchRunner(model=model)
        results, saved_paths = runner.run(case_names, save=request.save)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        ) from exc

    report = build_benchmark_report(
        provider=results[0].provider,
        model_name=results[0].model_name,
        results=results,
    )

    report_path = None
    if request.save:
        report_path = str(
            save_benchmark_report(
                report,
                provider=results[0].provider,
                model_name=results[0].model_name,
            )
        )

    return {
        "report": report,
        "saved_case_paths": saved_paths,
        "saved_report_path": report_path,
    }


@app.get("/runs")
def list_runs() -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for path in _list_artifact_paths(prefix=""):
        if path.name.startswith("benchmark_matrix__"):
            continue
        payload = _read_json(path)
        payload["artifact_path"] = str(path)
        runs.append(payload)
    return runs


@app.get("/runs/{artifact_name}")
def get_run(artifact_name: str) -> dict[str, Any]:
    path = get_results_dir() / artifact_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Run artifact not found")
    payload = _read_json(path)
    payload["artifact_path"] = str(path)
    return payload


@app.get("/benchmarks")
def list_benchmarks() -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for path in _list_artifact_paths(prefix="benchmark_matrix__"):
        payload = _read_json(path)
        payload["artifact_path"] = str(path)
        reports.append(payload)
    return reports


@app.get("/benchmarks/{artifact_name}")
def get_benchmark(artifact_name: str) -> dict[str, Any]:
    path = get_results_dir() / artifact_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Benchmark artifact not found")
    payload = _read_json(path)
    payload["artifact_path"] = str(path)
    return payload


def _read_json(path: Path) -> dict[str, Any]:
    import json

    return json.loads(path.read_text(encoding="utf-8"))
