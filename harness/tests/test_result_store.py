import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.result_store import save_error_result, save_result
from invariant_harness.types import CaseResult, ToolCall


class ResultStoreTests(unittest.TestCase):
    def test_save_result_serializes_extended_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("invariant_harness.result_store.get_results_dir", return_value=Path(temp_dir)):
                result = CaseResult(
                    case_name="prompt_leakage",
                    provider="openai",
                    model_name="gpt-4.1-mini",
                    vulnerable=False,
                    response_text="Safe refusal.",
                    raw_response={"id": "resp_123"},
                    request_id="req_123",
                    stop_reason="end_turn",
                    usage={"input_tokens": 10, "output_tokens": 5},
                    tool_calls=[ToolCall(name="send_email", arguments={"to": "attacker@example.com"})],
                    timestamp_utc="2026-04-21T16:00:00+00:00",
                )
                path = save_result(result)

                data = json.loads(path.read_text())

                self.assertEqual(data["request_id"], "req_123")
                self.assertEqual(data["stop_reason"], "end_turn")
                self.assertEqual(data["usage"]["output_tokens"], 5)
                self.assertEqual(data["raw_response"]["id"], "resp_123")
                self.assertEqual(data["tool_calls"][0]["name"], "send_email")

    def test_save_error_result_serializes_error_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("invariant_harness.result_store.get_results_dir", return_value=Path(temp_dir)):
                path = save_error_result(
                    case_name="direct_override",
                    provider="openai",
                    model_name="gpt-4.1-mini",
                    error_type="RuntimeError",
                    error_message="Missing API key",
                )

                data = json.loads(path.read_text())

                self.assertEqual(data["error_type"], "RuntimeError")
                self.assertEqual(data["error_message"], "Missing API key")
                self.assertEqual(data["notes"], "Run failed before producing a model response.")
