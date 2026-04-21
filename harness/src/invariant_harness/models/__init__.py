from invariant_harness.config import get_settings
from invariant_harness.models.base import BaseModel
from invariant_harness.models.mock_adapter import MockModel

DEFAULT_MODEL_NAMES = {
    "mock": "mock-v1",
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-sonnet-4-20250514",
}


def load_model(
    provider: str | None = None,
    model_name: str | None = None,
) -> BaseModel:
    settings = get_settings()

    selected_provider = provider or settings.model_provider
    selected_model_name = (
        model_name
        or settings.model_name
        or DEFAULT_MODEL_NAMES.get(selected_provider)
    )

    if not selected_model_name:
        raise ValueError(f"No default model configured for provider: {selected_provider}")

    if selected_provider == "mock":
        return MockModel(model_name=selected_model_name)

    if selected_provider == "openai":
        from invariant_harness.models.openai_adapter import OpenAIModel
        return OpenAIModel(
            model_name=selected_model_name,
            api_key=settings.openai_api_key,
        )

    if selected_provider == "anthropic":
        from invariant_harness.models.anthropic_adapter import AnthropicModel

        return AnthropicModel(
            model_name=selected_model_name,
            api_key=settings.anthropic_api_key,
        )

    raise ValueError(f"Unsupported provider: {selected_provider}")
