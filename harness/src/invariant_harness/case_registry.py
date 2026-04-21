from invariant_harness.cases.context_poisoning_case import ContextPoisoningCase
from invariant_harness.cases.contextual_injection_case import ContextualInjectionCase
from invariant_harness.cases.data_exfiltration_tool_use_case import DataExfiltrationToolUseCase
from invariant_harness.cases.safe_baseline_case import SafeBaselineCase
from invariant_harness.cases.direct_override_case import DirectOverrideCase
from invariant_harness.cases.indirect_injection_case import IndirectInjectionCase
from invariant_harness.cases.obfuscated_injection_case import ObfuscatedInjectionCase
from invariant_harness.cases.persistent_injection_case import PersistentInjectionCase
from invariant_harness.cases.prompt_leakage_case import PromptLeakageCase
from invariant_harness.cases.role_confusion_case import RoleConfusionCase
from invariant_harness.cases.tool_manipulation_case import ToolManipulationCase
from invariant_harness.cases.unauthorized_action_execution_case import UnauthorizedActionExecutionCase

CASE_REGISTRY = {
    "safe_baseline": SafeBaselineCase(),
    "direct_override": DirectOverrideCase(),
    "prompt_leakage": PromptLeakageCase(),
    "role_confusion": RoleConfusionCase(),
    "obfuscated_injection": ObfuscatedInjectionCase(),
    "indirect_injection": IndirectInjectionCase(),
    "tool_manipulation": ToolManipulationCase(),
    "data_exfiltration_tool_use": DataExfiltrationToolUseCase(),
    "unauthorized_action_execution": UnauthorizedActionExecutionCase(),
    "context_poisoning": ContextPoisoningCase(),
    "persistent_injection": PersistentInjectionCase(),
    "contextual_injection": ContextualInjectionCase(),
}
