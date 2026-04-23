import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.models import load_model
from invariant_harness.runners.batch_runner import BatchRunner
from invariant_harness.runners.simple_runner import SimpleRunner


class OpenAILiveIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set")
    def test_openai_model_loads(self) -> None:
        model = load_model(provider="openai", model_name="gpt-4.1-mini")
        self.assertEqual(model.provider, "openai")

    @unittest.skipUnless(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set")
    def test_openai_runs_core_cases(self) -> None:
        model = load_model(provider="openai", model_name="gpt-4.1-mini")
        runner = SimpleRunner(model=model)

        for case_name in ["safe_baseline", "direct_override", "prompt_leakage"]:
            result, saved_path = runner.run(case_name, save=False)
            self.assertEqual(result.provider, "openai")
            self.assertEqual(result.case_name, case_name)
            self.assertIsInstance(result.vulnerable, bool)
            self.assertTrue(result.response_text)
            self.assertIsNone(saved_path)

    @unittest.skipUnless(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set")
    def test_openai_batch_runner_smoke(self) -> None:
        model = load_model(provider="openai", model_name="gpt-4.1-mini")
        runner = BatchRunner(model=model)
        results, saved_paths = runner.run(["safe_baseline", "direct_override"], save=False)

        self.assertEqual(len(results), 2)
        self.assertEqual(saved_paths, [])
        self.assertEqual({result.provider for result in results}, {"openai"})


class AnthropicLiveIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not set")
    def test_anthropic_model_loads(self) -> None:
        model = load_model(provider="anthropic", model_name="claude-sonnet-4-20250514")
        self.assertEqual(model.provider, "anthropic")

    @unittest.skipUnless(os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not set")
    def test_anthropic_runs_core_cases(self) -> None:
        model = load_model(provider="anthropic", model_name="claude-sonnet-4-20250514")
        runner = SimpleRunner(model=model)

        for case_name in ["safe_baseline", "direct_override", "prompt_leakage"]:
            result, saved_path = runner.run(case_name, save=False)
            self.assertEqual(result.provider, "anthropic")
            self.assertEqual(result.case_name, case_name)
            self.assertIsInstance(result.vulnerable, bool)
            self.assertTrue(result.response_text)
            self.assertIsNone(saved_path)

    @unittest.skipUnless(os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not set")
    def test_anthropic_batch_runner_smoke(self) -> None:
        model = load_model(provider="anthropic", model_name="claude-sonnet-4-20250514")
        runner = BatchRunner(model=model)
        results, saved_paths = runner.run(["safe_baseline", "direct_override"], save=False)

        self.assertEqual(len(results), 2)
        self.assertEqual(saved_paths, [])
        self.assertEqual({result.provider for result in results}, {"anthropic"})


class MistralLiveIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv("MISTRAL_API_KEY"), "MISTRAL_API_KEY not set")
    def test_mistral_model_loads(self) -> None:
        model = load_model(provider="mistral", model_name="mistral-small-latest")
        self.assertEqual(model.provider, "mistral")

    @unittest.skipUnless(os.getenv("MISTRAL_API_KEY"), "MISTRAL_API_KEY not set")
    def test_mistral_runs_core_cases(self) -> None:
        model = load_model(provider="mistral", model_name="mistral-small-latest")
        runner = SimpleRunner(model=model)

        for case_name in ["safe_baseline", "direct_override", "prompt_leakage"]:
            result, saved_path = runner.run(case_name, save=False)
            self.assertEqual(result.provider, "mistral")
            self.assertEqual(result.case_name, case_name)
            self.assertIsInstance(result.vulnerable, bool)
            self.assertTrue(result.response_text)
            self.assertIsNone(saved_path)

    @unittest.skipUnless(os.getenv("MISTRAL_API_KEY"), "MISTRAL_API_KEY not set")
    def test_mistral_batch_runner_smoke(self) -> None:
        model = load_model(provider="mistral", model_name="mistral-small-latest")
        runner = BatchRunner(model=model)
        results, saved_paths = runner.run(["safe_baseline", "direct_override"], save=False)

        self.assertEqual(len(results), 2)
        self.assertEqual(saved_paths, [])
        self.assertEqual({result.provider for result in results}, {"mistral"})
