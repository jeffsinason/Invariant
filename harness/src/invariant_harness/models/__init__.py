from datetime import UTC, datetime, timedelta

from invariant_harness.config import get_settings
from invariant_harness.models.base import BaseModel
from invariant_harness.models.mock_adapter import MockModel

STATIC_SUPPORTED_MODELS = {
    "mock": [
        {
            "id": "mock-v1",
            "display_name": "Mock v1",
            "recommended_default": True,
            "recommended_for_harness": True,
        },
    ],
    "openai": [
        {
            "id": "gpt-4.1-mini",
            "display_name": "GPT-4.1 Mini",
            "recommended_default": True,
            "recommended_for_harness": True,
        },
        {
            "id": "gpt-4.1",
            "display_name": "GPT-4.1",
            "recommended_default": False,
            "recommended_for_harness": True,
        },
    ],
    "anthropic": [
        {
            "id": "claude-sonnet-4-20250514",
            "display_name": "Claude Sonnet 4",
            "recommended_default": True,
            "recommended_for_harness": True,
        },
        {
            "id": "claude-opus-4-20250514",
            "display_name": "Claude Opus 4",
            "recommended_default": False,
            "recommended_for_harness": True,
        },
    ],
    "mistral": [
        {
            "id": "mistral-small-latest",
            "display_name": "Mistral Small Latest",
            "recommended_default": True,
            "recommended_for_harness": True,
        },
        {
            "id": "mistral-large-latest",
            "display_name": "Mistral Large Latest",
            "recommended_default": False,
            "recommended_for_harness": True,
        },
    ],
}

DEFAULT_MODEL_NAMES = {
    "mock": "mock-v1",
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-sonnet-4-20250514",
    "mistral": "mistral-small-latest",
}

MODEL_CACHE_TTL = timedelta(minutes=5)
_LIVE_MODEL_CACHE: dict[str, tuple[datetime, list[dict[str, str | bool]]]] = {}


def _model_sort_key(model: dict[str, str | bool]) -> tuple[int, str]:
    return (0 if bool(model.get("recommended_default")) else 1, str(model["id"]))


def _normalize_model(
    provider: str,
    model_id: str,
    display_name: str | None = None,
    source: str = "static",
    recommended_for_harness: bool = False,
) -> dict[str, str | bool]:
    return {
        "provider": provider,
        "id": model_id,
        "display_name": display_name or model_id,
        "recommended_default": model_id == DEFAULT_MODEL_NAMES.get(provider),
        "recommended_for_harness": recommended_for_harness,
        "source": source,
    }


def _get_static_models(provider: str) -> list[dict[str, str | bool]]:
    return [
        _normalize_model(
            provider=provider,
            model_id=str(model["id"]),
            display_name=str(model["display_name"]),
            source="static",
            recommended_for_harness=bool(model.get("recommended_for_harness", False)),
        )
        for model in STATIC_SUPPORTED_MODELS.get(provider, [])
    ]


def _get_cached_live_models(provider: str) -> list[dict[str, str | bool]] | None:
    cached = _LIVE_MODEL_CACHE.get(provider)
    if not cached:
        return None

    cached_at, models = cached
    if datetime.now(UTC) - cached_at > MODEL_CACHE_TTL:
        _LIVE_MODEL_CACHE.pop(provider, None)
        return None

    return models


def _set_cached_live_models(provider: str, models: list[dict[str, str | bool]]) -> None:
    _LIVE_MODEL_CACHE[provider] = (datetime.now(UTC), models)


def _discover_openai_models(api_key: str) -> list[dict[str, str | bool]]:
    if not api_key:
        return []

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    models = []
    for model in client.models.list():
        models.append(
            _normalize_model(
                provider="openai",
                model_id=model.id,
                display_name=model.id,
                source="live",
                recommended_for_harness=False,
            )
        )
    return sorted(models, key=_model_sort_key)


def _discover_anthropic_models(api_key: str) -> list[dict[str, str | bool]]:
    if not api_key:
        return []

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    page = client.models.list(limit=1000)
    models = [
        _normalize_model(
            provider="anthropic",
            model_id=model.id,
            display_name=getattr(model, "display_name", None) or model.id,
            source="live",
            recommended_for_harness=False,
        )
        for model in page.data
    ]
    return sorted(models, key=_model_sort_key)


def _discover_live_models(provider: str) -> list[dict[str, str | bool]]:
    cached = _get_cached_live_models(provider)
    if cached is not None:
        return cached

    settings = get_settings()
    if provider == "mock":
        live_models = _get_static_models("mock")
    elif provider == "openai":
        live_models = _discover_openai_models(settings.openai_api_key)
    elif provider == "anthropic":
        live_models = _discover_anthropic_models(settings.anthropic_api_key)
    elif provider == "mistral":
        live_models = _discover_mistral_models(settings.mistral_api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    if live_models or provider == "mock":
        _set_cached_live_models(provider, live_models)
    return live_models


def _discover_mistral_models(api_key: str) -> list[dict[str, str | bool]]:
    if not api_key:
        return []

    from mistralai.client import Mistral

    client = Mistral(api_key=api_key)
    response = client.models.list()
    models = []
    for model in response.data or []:
        if getattr(model, "deprecation", None):
            continue

        models.append(
            _normalize_model(
                provider="mistral",
                model_id=model.id,
                display_name=getattr(model, "name", None) or model.id,
                source="live",
                recommended_for_harness=False,
            )
        )

    return sorted(models, key=_model_sort_key)


def _merge_models(
    provider: str,
    static_models: list[dict[str, str | bool]],
    live_models: list[dict[str, str | bool]],
) -> list[dict[str, str | bool]]:
    merged: dict[str, dict[str, str | bool]] = {}
    for model in live_models:
        merged[str(model["id"])] = dict(model)
    for model in static_models:
        model_id = str(model["id"])
        if model_id in merged:
            merged[model_id] = {**merged[model_id], **model}
        else:
            merged[model_id] = dict(model)

    result = list(merged.values())
    for model in result:
        model["recommended_default"] = str(model["id"]) == DEFAULT_MODEL_NAMES.get(provider)
        if "recommended_for_harness" not in model:
            model["recommended_for_harness"] = False
    return sorted(result, key=_model_sort_key)


def list_supported_models(
    provider: str | None = None,
    include_live: bool = True,
) -> list[dict[str, str | bool]]:
    if provider:
        if provider not in STATIC_SUPPORTED_MODELS:
            raise ValueError(f"Unsupported provider: {provider}")

        static_models = _get_static_models(provider)
        if not include_live:
            return static_models

        try:
            live_models = _discover_live_models(provider)
        except Exception:
            live_models = []
        return _merge_models(provider, static_models, live_models)

    all_models: list[dict[str, str | bool]] = []
    for provider_name in STATIC_SUPPORTED_MODELS:
        all_models.extend(list_supported_models(provider=provider_name, include_live=include_live))
    return all_models


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

    if selected_provider == "mistral":
        from invariant_harness.models.mistral_adapter import MistralModel

        return MistralModel(
            model_name=selected_model_name,
            api_key=settings.mistral_api_key,
        )

    raise ValueError(f"Unsupported provider: {selected_provider}")
