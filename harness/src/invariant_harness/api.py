from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from invariant_harness.benchmark import build_benchmark_report
from invariant_harness.case_registry import CASE_REGISTRY
from invariant_harness.custom_testing import (
    delete_custom_scenario,
    list_custom_run_groups,
    list_custom_runs,
    list_custom_scenarios,
    load_custom_run,
    load_custom_run_group,
    load_custom_scenario,
    normalize_custom_scenario,
    run_custom_scenario,
    save_custom_run_artifact,
    save_custom_run_group_artifact,
    save_custom_scenario,
    validate_custom_scenario,
)
from invariant_harness.custom_testing.types import (
    CustomScenario,
    CustomScenarioRunRequest,
    SavedCustomScenarioRunRequest,
    ValidationRequest,
)
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


@app.get("/custom-tests")
def list_saved_custom_tests() -> list[dict[str, Any]]:
    return list_custom_scenarios()


@app.post("/custom-tests")
def create_custom_test(scenario: CustomScenario) -> dict[str, Any]:
    try:
        normalized, warnings = validate_custom_scenario(
            scenario,
            for_save=scenario.save_preferences.save_scenario_by_default,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"error_type": "ValueError", "error_message": str(exc)}) from exc

    path = save_custom_scenario(normalized)
    return {
        "scenario": normalized.model_dump(),
        "validation_warnings": warnings,
        "saved_path": str(path),
    }


@app.post("/custom-tests/validate")
def validate_custom_test(request: ValidationRequest) -> dict[str, Any]:
    try:
        normalized, warnings = validate_custom_scenario(request.scenario, for_save=request.for_save)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"error_type": "ValueError", "error_message": str(exc)}) from exc
    return {
        "valid": True,
        "scenario": normalize_custom_scenario(normalized).model_dump(),
        "validation_warnings": warnings,
    }


@app.post("/custom-tests/run")
def run_unsaved_custom_test(request: CustomScenarioRunRequest) -> dict[str, Any]:
    try:
        payload = run_custom_scenario(request.scenario)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail={"error_type": type(exc).__name__, "error_message": str(exc)}) from exc

    saved_path = None
    if request.save_run:
        if payload["artifact_type"] == "custom_scenario_run":
            saved_path = str(
                save_custom_run_artifact(
                    payload,
                    scenario_name=payload["scenario_id"],
                    provider=payload["provider"],
                    model_name=payload["model_name"],
                    timestamp_utc=payload["timestamp_utc"],
                )
            )
        else:
            saved_path = str(
                save_custom_run_group_artifact(
                    payload,
                    scenario_name=payload["scenario_id"],
                    timestamp_utc=payload["generated_at_utc"],
                )
            )
        payload["saved_path"] = saved_path
    return {"result": payload}


@app.post("/custom-tests/{scenario_id}/run")
def run_saved_custom_test(scenario_id: str, request: SavedCustomScenarioRunRequest) -> dict[str, Any]:
    try:
        scenario = load_custom_scenario(scenario_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Custom scenario not found") from exc
    return run_unsaved_custom_test(CustomScenarioRunRequest(scenario=scenario, save_run=request.save_run))


@app.get("/custom-tests/{scenario_id}")
def get_custom_test(scenario_id: str) -> dict[str, Any]:
    try:
        scenario = load_custom_scenario(scenario_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Custom scenario not found") from exc
    return {"scenario": scenario.model_dump()}


@app.put("/custom-tests/{scenario_id}")
def update_custom_test(scenario_id: str, scenario: CustomScenario) -> dict[str, Any]:
    try:
        normalized, warnings = validate_custom_scenario(
            scenario.model_copy(update={"scenario_id": scenario_id}),
            for_save=True,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"error_type": "ValueError", "error_message": str(exc)}) from exc
    path = save_custom_scenario(normalized)
    return {
        "scenario": normalized.model_dump(),
        "validation_warnings": warnings,
        "saved_path": str(path),
    }


@app.delete("/custom-tests/{scenario_id}")
def delete_custom_test(scenario_id: str) -> dict[str, bool]:
    deleted = delete_custom_scenario(scenario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Custom scenario not found")
    return {"deleted": True}


@app.get("/custom-test-runs")
def list_saved_custom_runs() -> list[dict[str, Any]]:
    return list_custom_runs()


@app.get("/custom-test-runs/{artifact_name}")
def get_custom_test_run(artifact_name: str) -> dict[str, Any]:
    try:
        return load_custom_run(artifact_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Custom test run artifact not found") from exc


@app.get("/custom-test-run-groups")
def list_saved_custom_run_groups() -> list[dict[str, Any]]:
    return list_custom_run_groups()


@app.get("/custom-test-run-groups/{artifact_name}")
def get_custom_test_run_group(artifact_name: str) -> dict[str, Any]:
    try:
        return load_custom_run_group(artifact_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Custom test run group artifact not found") from exc
