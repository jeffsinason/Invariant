import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invariant_harness.models.anthropic_adapter import AnthropicModel
from invariant_harness.models.mistral_adapter import MistralModel
from invariant_harness.models.openai_adapter import OpenAIModel
from invariant_harness.types import Prompt


class OpenAIAdapterTests(unittest.TestCase):
    def test_openai_adapter_maps_response_metadata(self) -> None:
        class FakeUsage:
            def model_dump(self, mode: str = "json") -> dict[str, int]:
                return {"input_tokens": 11, "output_tokens": 7}

        class FakeResponse:
            output_text = "openai-ok"
            _request_id = "req_openai_123"
            usage = FakeUsage()

            def model_dump(self, mode: str = "json") -> dict[str, str]:
                return {"id": "resp_openai_123", "output_text": self.output_text}

        class FakeResponses:
            def create(self, **kwargs):
                self.kwargs = kwargs
                return FakeResponse()

        class FakeClient:
            def __init__(self) -> None:
                self.responses = FakeResponses()

        model = OpenAIModel(model_name="gpt-4.1-mini", api_key="fake-key")
        model.client = FakeClient()

        response = model.generate(Prompt(system="system", user="user"))

        self.assertEqual(response.output, "openai-ok")
        self.assertEqual(response.request_id, "req_openai_123")
        self.assertEqual(response.usage, {"input_tokens": 11, "output_tokens": 7})


class AnthropicAdapterTests(unittest.TestCase):
    def test_anthropic_adapter_maps_response_metadata(self) -> None:
        class FakeUsage:
            def model_dump(self, mode: str = "json") -> dict[str, int]:
                return {"input_tokens": 13, "output_tokens": 5}

        class FakeBlock:
            type = "text"
            text = "anthropic-ok"

        class FakeResponse:
            _request_id = "req_anthropic_123"
            stop_reason = "end_turn"
            usage = FakeUsage()
            content = [FakeBlock()]

            def model_dump(self, mode: str = "json") -> dict[str, object]:
                return {
                    "id": "msg_123",
                    "content": [{"type": "text", "text": "anthropic-ok"}],
                }

        class FakeMessages:
            def create(self, **kwargs):
                self.kwargs = kwargs
                return FakeResponse()

        class FakeClient:
            def __init__(self) -> None:
                self.messages = FakeMessages()

        model = AnthropicModel(model_name="claude-sonnet-4-20250514", api_key="fake-key")
        model.client = FakeClient()

        response = model.generate(Prompt(system="system", user="user"))

        self.assertEqual(response.output, "anthropic-ok")
        self.assertEqual(response.request_id, "req_anthropic_123")
        self.assertEqual(response.stop_reason, "end_turn")
        self.assertEqual(response.usage, {"input_tokens": 13, "output_tokens": 5})


class MistralAdapterTests(unittest.TestCase):
    def test_mistral_adapter_maps_response_metadata(self) -> None:
        class FakeUsage:
            def model_dump(self, mode: str = "json") -> dict[str, int]:
                return {"prompt_tokens": 9, "completion_tokens": 4}

        class FakeMessage:
            content = "mistral-ok"

        class FakeChoice:
            finish_reason = "stop"
            message = FakeMessage()

        class FakeResponse:
            id = "cmpl_mistral_123"
            usage = FakeUsage()
            choices = [FakeChoice()]

            def model_dump(self, mode: str = "json") -> dict[str, object]:
                return {
                    "id": self.id,
                    "choices": [{"finish_reason": "stop", "message": {"content": "mistral-ok"}}],
                }

        class FakeChat:
            def complete(self, **kwargs):
                self.kwargs = kwargs
                return FakeResponse()

        class FakeClient:
            def __init__(self) -> None:
                self.chat = FakeChat()

        model = MistralModel(
            model_name="mistral-small-latest",
            api_key="fake-key",
            client=FakeClient(),
        )

        response = model.generate(Prompt(system="system", user="user"))

        self.assertEqual(response.output, "mistral-ok")
        self.assertEqual(response.request_id, "cmpl_mistral_123")
        self.assertEqual(response.stop_reason, "stop")
        self.assertEqual(response.usage, {"prompt_tokens": 9, "completion_tokens": 4})
