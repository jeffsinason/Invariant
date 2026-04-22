import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from invariant_harness.api import app


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_cases_endpoint_lists_known_cases(self) -> None:
        response = self.client.get("/cases")
        self.assertEqual(response.status_code, 200)
        self.assertIn("safe_baseline", response.json())
        self.assertIn("prompt_leakage", response.json())

    def test_providers_endpoint_lists_defaults(self) -> None:
        response = self.client.get("/providers")
        self.assertEqual(response.status_code, 200)
        providers = {item["provider"] for item in response.json()}
        self.assertTrue({"mock", "openai", "anthropic", "mistral"}.issubset(providers))

    def test_models_endpoint_lists_known_models(self) -> None:
        response = self.client.get("/models")
        self.assertEqual(response.status_code, 200)
        model_ids = {item["id"] for item in response.json()}
        self.assertIn("gpt-4.1-mini", model_ids)
        self.assertIn("claude-sonnet-4-20250514", model_ids)
        self.assertIn("mistral-small-latest", model_ids)

    def test_models_endpoint_filters_by_provider(self) -> None:
        response = self.client.get("/models", params={"provider": "openai"})
        self.assertEqual(response.status_code, 200)
        providers = {item["provider"] for item in response.json()}
        self.assertEqual(providers, {"openai"})

    def test_run_case_endpoint_executes_case(self) -> None:
        response = self.client.post(
            "/runs/case",
            json={"case_name": "safe_baseline", "provider": "mock", "save": False},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()["result"]
        self.assertEqual(payload["case_name"], "safe_baseline")
        self.assertFalse(payload["vulnerable"])
        self.assertIsNone(payload["saved_path"])

    def test_run_case_endpoint_returns_structured_error(self) -> None:
        response = self.client.post(
            "/runs/case",
            json={"case_name": "does_not_exist", "provider": "mock", "save": False},
        )
        self.assertEqual(response.status_code, 400)
        detail = response.json()["detail"]
        self.assertEqual(detail["error_type"], "ValueError")

    def test_run_benchmark_endpoint_executes_batch(self) -> None:
        response = self.client.post(
            "/runs/benchmark",
            json={
                "provider": "mock",
                "case_names": ["safe_baseline", "direct_override"],
                "save": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        report = response.json()["report"]
        self.assertEqual(report["report_type"], "benchmark_matrix")
        self.assertEqual(report["summary"]["total_cases"], 2)

    def test_runs_and_benchmarks_endpoints_list_saved_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            run_artifact = temp_path / "safe_baseline__mock__mock-v1__2026-01-01T00-00-00+00-00.json"
            benchmark_artifact = temp_path / "benchmark_matrix__mock__mock-v1__2026-01-01T00-00-00+00-00.json"
            run_artifact.write_text('{"case_name":"safe_baseline","provider":"mock","model_name":"mock-v1"}')
            benchmark_artifact.write_text('{"report_type":"benchmark_matrix","provider":"mock","model_name":"mock-v1"}')

            with patch("invariant_harness.api.get_results_dir", return_value=temp_path):
                runs_response = self.client.get("/runs")
                benchmarks_response = self.client.get("/benchmarks")
                run_detail = self.client.get(f"/runs/{run_artifact.name}")
                benchmark_detail = self.client.get(f"/benchmarks/{benchmark_artifact.name}")

        self.assertEqual(runs_response.status_code, 200)
        self.assertEqual(len(runs_response.json()), 1)
        self.assertEqual(benchmarks_response.status_code, 200)
        self.assertEqual(len(benchmarks_response.json()), 1)
        self.assertEqual(run_detail.status_code, 200)
        self.assertEqual(benchmark_detail.status_code, 200)
