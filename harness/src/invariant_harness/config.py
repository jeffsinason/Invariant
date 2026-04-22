import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    model_provider: str
    model_name: str
    openai_api_key: str
    anthropic_api_key: str
    mistral_api_key: str


def get_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")
    load_dotenv()

    return Settings(
        model_provider=os.getenv("MODEL_PROVIDER", "mock"),
        model_name=os.getenv("MODEL_NAME", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
