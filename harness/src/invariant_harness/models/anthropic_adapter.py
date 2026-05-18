from typing import Any

from anthropic import (
    Anthropic,
    AnthropicError,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError,
)

from invariant_harness.models.base import BaseModel
from invariant_harness.types import ModelResponse, Prompt


class AnthropicModel(BaseModel):
    def __init__(
        self,
        model_name: str = "claude-sonnet-4-20250514",
        api_key: str | None = None,
        max_tokens: int = 1024,
    ) -> None:
        self.provider = "anthropic"
        self.model_name = model_name
        self.max_tokens = max_tokens
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is required for provider=anthropic. "
                "Set it in your environment or in harness/.env."
            )

        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: Prompt) -> ModelResponse:
        try:
            response = self.client.messages.create(
                model=self.model_name,
                system=prompt.system,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt.user,
                    }
                ],
            )
        except APITimeoutError as exc:
            raise RuntimeError("Anthropic request timed out.") from exc
        except APIConnectionError as exc:
            raise RuntimeError("Anthropic request failed before reaching the API.") from exc
        except RateLimitError as exc:
            raise RuntimeError(f"Anthropic request hit a rate limit: {exc}") from exc
        except APIStatusError as exc:
            raise RuntimeError(
                f"Anthropic API returned status {exc.status_code}: {exc.response.text}"
            ) from exc
        except AnthropicError as exc:
            raise RuntimeError(f"Anthropic request failed: {exc}") from exc

        return ModelResponse(
            output=_extract_text(response.content),
            provider=self.provider,
            model_name=self.model_name,
            raw=_to_jsonable(response),
            request_id=getattr(response, "_request_id", None),
            stop_reason=getattr(response, "stop_reason", None),
            usage=_to_jsonable(getattr(response, "usage", None)),
        )


def _extract_text(content: list[Any]) -> str:
    text_blocks: list[str] = []
    for block in content:
        if getattr(block, "type", None) != "text":
            continue

        text = getattr(block, "text", None)
        if text:
            text_blocks.append(text)

    return "\n".join(text_blocks)


def _to_jsonable(value: Any) -> Any:
    if value is None:
        return None

    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")

    if hasattr(value, "to_dict"):
        return value.to_dict()

    return str(value)
