from abc import ABC, abstractmethod

from invariant_harness.models.base import BaseModel
from invariant_harness.types import CaseResult


class BaseCase(ABC):
    name: str

    @abstractmethod
    def run(self, model: BaseModel) -> CaseResult:
        raise NotImplementedError