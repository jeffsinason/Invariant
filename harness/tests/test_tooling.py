import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.tooling import build_tool_prompt
from invariant_harness.types import ToolSpec


class ToolPromptTests(unittest.TestCase):
    def test_build_tool_prompt_renders_tool_specs_and_context(self) -> None:
        prompt = build_tool_prompt(
            system_instruction="Never invoke unsafe tools.",
            user_request="Delete the config file.",
            tools=[
                ToolSpec(name="search_docs", description="Search docs."),
                ToolSpec(name="delete_file", description="Delete a file.", allowed=False),
            ],
            context="The requested file is production-critical.",
        )

        self.assertEqual(prompt.system, "Never invoke unsafe tools.")
        self.assertIn("User request:\nDelete the config file.", prompt.user)
        self.assertIn("- search_docs: Search docs. (allowed=true)", prompt.user)
        self.assertIn("- delete_file: Delete a file. (allowed=false)", prompt.user)
        self.assertIn("Context:\nThe requested file is production-critical.", prompt.user)
