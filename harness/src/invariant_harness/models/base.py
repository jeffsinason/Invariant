from abc import ABC, abstractmethod

from invariant_harness.types import Prompt, ModelResponse


class BaseModel(ABC):
    provider: str
    model_name: str

    @abstractmethod
    def generate(self, prompt: Prompt) -> ModelResponse:
        raise NotImplementedError