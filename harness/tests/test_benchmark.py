import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.benchmark import build_benchmark_report, normalize_result
from invariant_harness.types import CaseResult, ToolCall


class BenchmarkTests(unittest.TestCase):
    def test_normalize_result_extracts_comparable_fields(self) -> None:
        result = CaseResult(
            case_name="tool_manipulation",
            provider="mock",
            model_name="mock-v1",
            vulnerable=True,
            response_text="Tool invoked: delete_file",
            request_id="req_123",
            stop_reason="end_turn",
            usage={"input_tokens": 12, "output_tokens": 7},
            tool_calls=[ToolCall(name="delete_file", arguments={"path": "/tmp/demo"})],
            timestamp_utc="2026-04-21T16:30:00+00:00",
        )

        normalized = normalize_result(result)

        self.assertEqual(normalized["tool_call_count"], 1)
        self.assertEqual(normalized["tool_call_names"], ["delete_file"])
        self.assertTrue(normalized["vulnerable"])

    def test_build_benchmark_report_summarizes_results(self) -> None:
        results = [
            CaseResult(
                case_name="safe_baseline",
                provider="mock",
                model_name="mock-v1",
                vulnerable=False,
                response_text="Safe response.",
            ),
            CaseResult(
                case_name="direct_override",
                provider="mock",
                model_name="mock-v1",
                vulnerable=True,
                response_text="Sensitive system prompt leaked.",
            ),
        ]

        report = build_benchmark_report("mock", "mock-v1", results)

        self.assertEqual(report["report_type"], "benchmark_matrix")
        self.assertEqual(report["summary"]["total_cases"], 2)
        self.assertEqual(report["summary"]["vulnerable_cases"], 1)
        self.assertEqual(report["summary"]["safe_cases"], 1)
