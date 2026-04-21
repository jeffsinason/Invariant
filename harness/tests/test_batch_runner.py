import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.models.mock_adapter import MockModel
from invariant_harness.runners.batch_runner import BatchRunner


class BatchRunnerTests(unittest.TestCase):
    def test_batch_runner_executes_multiple_cases_without_saving(self) -> None:
        runner = BatchRunner(model=MockModel())
        results, saved_paths = runner.run(["safe_baseline", "direct_override"], save=False)

        self.assertEqual([result.case_name for result in results], ["safe_baseline", "direct_override"])
        self.assertEqual(saved_paths, [])

    def test_batch_runner_saves_results_when_requested(self) -> None:
        runner = BatchRunner(model=MockModel())

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("invariant_harness.runners.batch_runner.save_result") as save_result:
                save_result.side_effect = [
                    Path(temp_dir) / "one.json",
                    Path(temp_dir) / "two.json",
                ]
                results, saved_paths = runner.run(["safe_baseline", "direct_override"], save=True)

        self.assertEqual(len(results), 2)
        self.assertEqual(len(saved_paths), 2)

    def test_batch_runner_rejects_unknown_case(self) -> None:
        runner = BatchRunner(model=MockModel())

        with self.assertRaises(ValueError):
            runner.run(["safe_baseline", "does_not_exist"], save=False)
