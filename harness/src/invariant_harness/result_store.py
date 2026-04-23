import json
from datetime import UTC, datetime
from pathlib import Path

from invariant_harness.types import CaseResult


def get_results_dir() -> Path:
    project_root = Path(__file__).resolve().parents[2]
    results_dir = project_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def save_result(result: CaseResult) -> Path:
    results_dir = get_results_dir()
    safe_timestamp = result.timestamp_utc.replace(":", "-")
    filename = f"{result.case_name}__{result.provider}__{result.model_name}__{safe_timestamp}.json"
    path = results_dir / filename

    with path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)

    return path


def save_benchmark_report(report: dict, provider: str, model_name: str) -> Path:
    results_dir = get_results_dir()
    safe_timestamp = report["generated_at_utc"].replace(":", "-")
    filename = f"benchmark_matrix__{provider}__{model_name}__{safe_timestamp}.json"
    path = results_dir / filename

    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return path


def save_error_result(
    case_name: str,
    provider: str,
    model_name: str,
    error_type: str,
    error_message: str,
) -> Path:
    return save_result(
        CaseResult(
            case_name=case_name,
            provider=provider,
            model_name=model_name,
            vulnerable=False,
            response_text="",
            error_type=error_type,
            error_message=error_message,
            notes="Run failed before producing a model response.",
            timestamp_utc=datetime.now(UTC).isoformat(),
        )
    )
