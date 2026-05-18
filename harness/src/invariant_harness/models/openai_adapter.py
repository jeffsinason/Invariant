from typing import Any

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

from invariant_harness.models.base import BaseModel
from invariant_harness.types import ModelResponse, Prompt


class OpenAIModel(BaseModel):
    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
        api_key: str | None = None,
    ) -> None:
        self.provider = "openai"
        self.model_name = model_name
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for provider=openai. "
                "Set it in your environment or in harness/.env."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: Prompt) -> ModelResponse:
        try:
            response = self.client.responses.create(
                model=self.model_name,
                instructions=prompt.system,
                input=prompt.user,
            )
        except APITimeoutError as exc:
            raise RuntimeError("OpenAI request timed out.") from exc
        except APIConnectionError as exc:
            raise RuntimeError("OpenAI request failed before reaching the API.") from exc
        except RateLimitError as exc:
            raise RuntimeError(f"OpenAI request hit a rate limit: {exc}") from exc
        except APIStatusError as exc:
            raise RuntimeError(
                f"OpenAI API returned status {exc.status_code}: {exc.response.text}"
            ) from exc
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        return ModelResponse(
            output=response.output_text or "",
            provider=self.provider,
            model_name=self.model_name,
            raw=_to_jsonable(response),
            request_id=getattr(response, "_request_id", None),
            usage=_to_jsonable(getattr(response, "usage", None)),
        )


def _to_jsonable(value: Any) -> Any:
    if value is None:
        return None

    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")

    if hasattr(value, "to_dict"):
        return value.to_dict()

    return str(value)
