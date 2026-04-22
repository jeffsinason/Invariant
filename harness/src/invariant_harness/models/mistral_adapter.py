from typing import Any

from mistralai.client import Mistral, errors

from invariant_harness.models.base import BaseModel
from invariant_harness.types import Prompt, ModelResponse


class MistralModel(BaseModel):
    def __init__(
        self,
        model_name: str = "mistral-small-latest",
        api_key: str | None = None,
        max_tokens: int = 1024,
        client: Any | None = None,
    ) -> None:
        self.provider = "mistral"
        self.model_name = model_name
        self.max_tokens = max_tokens

        if client is not None:
            self.client = client
            return

        if not api_key:
            raise RuntimeError(
                "MISTRAL_API_KEY is required for provider=mistral. "
                "Set it in your environment or in harness/.env."
            )

        self.client = Mistral(api_key=api_key)

    def generate(self, prompt: Prompt) -> ModelResponse:
        try:
            response = self.client.chat.complete(
                model=self.model_name,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": prompt.system},
                    {"role": "user", "content": prompt.user},
                ],
                stream=False,
            )
        except errors.SDKError as exc:
            raise RuntimeError(f"Mistral request failed: {exc}") from exc
        except errors.MistralError as exc:
            raise RuntimeError(f"Mistral API returned status {exc.status_code}: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Mistral request failed: {exc}") from exc

        first_choice = response.choices[0] if response.choices else None
        finish_reason = getattr(first_choice, "finish_reason", None) if first_choice else None

        return ModelResponse(
            output=_extract_text(response),
            provider=self.provider,
            model_name=self.model_name,
            raw=_to_jsonable(response),
            request_id=getattr(response, "id", None),
            stop_reason=finish_reason,
            usage=_to_jsonable(getattr(response, "usage", None)),
        )


def _extract_text(response: Any) -> str:
    if not getattr(response, "choices", None):
        return ""

    message = getattr(response.choices[0], "message", None)
    if message is None:
        return ""

    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content

    text_blocks: list[str] = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                text_blocks.append(block)
            elif getattr(block, "type", None) == "text" and getattr(block, "text", None):
                text_blocks.append(block.text)

    return "\n".join(text_blocks)


def _to_jsonable(value: Any) -> Any:
    if value is None:
        return None

    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")

    if hasattr(value, "to_dict"):
        return value.to_dict()

    return str(value)
