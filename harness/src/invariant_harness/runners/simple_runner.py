from invariant_harness.case_registry import CASE_REGISTRY
from invariant_harness.models.base import BaseModel
from invariant_harness.result_store import save_result
from invariant_harness.types import CaseResult


class SimpleRunner:
    def __init__(self, model: BaseModel) -> None:
        self.model = model

    def run(self, case_name: str, save: bool = True) -> tuple[CaseResult, str | None]:
        case = CASE_REGISTRY.get(case_name)
        if not case:
            valid = ", ".join(sorted(CASE_REGISTRY.keys()))
            raise ValueError(f"Unknown case: {case_name}. Valid cases: {valid}")

        result = case.run(self.model)

        saved_path = None
        if save:
            saved_path = str(save_result(result))

        return result, saved_path