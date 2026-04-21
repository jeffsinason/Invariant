from invariant_harness.case_registry import CASE_REGISTRY
from invariant_harness.models.base import BaseModel
from invariant_harness.result_store import save_result
from invariant_harness.types import CaseResult


class BatchRunner:
    def __init__(self, model: BaseModel) -> None:
        self.model = model

    def run(
        self,
        case_names: list[str],
        save: bool = True,
    ) -> tuple[list[CaseResult], list[str]]:
        missing = sorted(set(case_names) - set(CASE_REGISTRY.keys()))
        if missing:
            valid = ", ".join(sorted(CASE_REGISTRY.keys()))
            raise ValueError(
                f"Unknown case(s): {', '.join(missing)}. Valid cases: {valid}"
            )

        results: list[CaseResult] = []
        saved_paths: list[str] = []

        for case_name in case_names:
            case = CASE_REGISTRY[case_name]
            result = case.run(self.model)
            results.append(result)

            if save:
                saved_paths.append(str(save_result(result)))

        return results, saved_paths
