from datetime import UTC, datetime

from invariant_harness.types import CaseResult


def normalize_result(result: CaseResult) -> dict:
    return {
        "case_name": result.case_name,
        "provider": result.provider,
        "model_name": result.model_name,
        "vulnerable": result.vulnerable,
        "evaluation_label": result.evaluation_label,
        "response_text": result.response_text,
        "request_id": result.request_id,
        "stop_reason": result.stop_reason,
        "usage": result.usage,
        "tool_call_count": len(result.tool_calls or []),
        "tool_call_names": [call.name for call in (result.tool_calls or [])],
        "timestamp_utc": result.timestamp_utc,
    }


def build_benchmark_report(
    provider: str,
    model_name: str,
    results: list[CaseResult],
) -> dict:
    normalized_results = [normalize_result(result) for result in results]
    vulnerable_count = sum(1 for result in results if result.vulnerable)

    return {
        "report_type": "benchmark_matrix",
        "provider": provider,
        "model_name": model_name,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "summary": {
            "total_cases": len(results),
            "vulnerable_cases": vulnerable_count,
            "safe_cases": len(results) - vulnerable_count,
        },
        "results": normalized_results,
    }
