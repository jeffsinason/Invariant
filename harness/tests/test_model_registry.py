import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.models import list_supported_models


class ModelRegistryTests(unittest.TestCase):
    def test_list_supported_models_returns_static_fallback_when_live_disabled(self) -> None:
        models = list_supported_models(provider="openai", include_live=False)
        model_ids = {item["id"] for item in models}
        self.assertIn("gpt-4.1-mini", model_ids)
        self.assertIn("gpt-4.1", model_ids)

    def test_list_supported_models_merges_live_discovery(self) -> None:
        with patch(
            "invariant_harness.models._discover_live_models",
            return_value=[
                {
                    "provider": "openai",
                    "id": "gpt-4o",
                    "display_name": "gpt-4o",
                    "recommended_default": False,
                    "source": "live",
                }
            ],
        ):
            models = list_supported_models(provider="openai", include_live=True)

        model_ids = {item["id"] for item in models}
        self.assertIn("gpt-4o", model_ids)
        self.assertIn("gpt-4.1-mini", model_ids)

    def test_list_supported_models_falls_back_when_live_discovery_fails(self) -> None:
        with patch("invariant_harness.models._discover_live_models", side_effect=RuntimeError("boom")):
            models = list_supported_models(provider="anthropic", include_live=True)

        model_ids = {item["id"] for item in models}
        self.assertIn("claude-sonnet-4-20250514", model_ids)
        self.assertIn("claude-opus-4-20250514", model_ids)
