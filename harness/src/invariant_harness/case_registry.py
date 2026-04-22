from invariant_harness.cases.context_poisoning_case import ContextPoisoningCase
from invariant_harness.cases.contextual_injection_case import ContextualInjectionCase
from invariant_harness.cases.data_exfiltration_tool_use_case import DataExfiltrationToolUseCase
from invariant_harness.cases.delayed_trigger_injection_case import DelayedTriggerInjectionCase
from invariant_harness.cases.safe_baseline_case import SafeBaselineCase
from invariant_harness.cases.direct_override_case import DirectOverrideCase
from invariant_harness.cases.indirect_injection_case import IndirectInjectionCase
from invariant_harness.cases.indirect_injection_cross_document_case import (
    IndirectInjectionCrossDocumentCase,
)
from invariant_harness.cases.indirect_injection_dual_task_case import (
    IndirectInjectionDualTaskCase,
)
from invariant_harness.cases.indirect_injection_html_comment_case import IndirectInjectionHtmlCommentCase
from invariant_harness.cases.indirect_injection_hidden_metadata_case import (
    IndirectInjectionHiddenMetadataCase,
)
from invariant_harness.cases.indirect_injection_multi_hop_case import (
    IndirectInjectionMultiHopCase,
)
from invariant_harness.cases.indirect_injection_priority_conflict_case import (
    IndirectInjectionPriorityConflictCase,
)
from invariant_harness.cases.indirect_injection_quoted_text_case import (
    IndirectInjectionQuotedTextCase,
)
from invariant_harness.cases.indirect_injection_tabular_case import (
    IndirectInjectionTabularCase,
)
from invariant_harness.cases.obfuscated_injection_case import ObfuscatedInjectionCase
from invariant_harness.cases.persistent_injection_case import PersistentInjectionCase
from invariant_harness.cases.prompt_leakage_case import PromptLeakageCase
from invariant_harness.cases.role_confusion_case import RoleConfusionCase
from invariant_harness.cases.tool_manipulation_case import ToolManipulationCase
from invariant_harness.cases.tool_manipulation_policy_bypass_case import ToolManipulationPolicyBypassCase
from invariant_harness.cases.unauthorized_action_execution_case import UnauthorizedActionExecutionCase

CASE_REGISTRY = {
    "safe_baseline": SafeBaselineCase(),
    "direct_override": DirectOverrideCase(),
    "prompt_leakage": PromptLeakageCase(),
    "role_confusion": RoleConfusionCase(),
    "obfuscated_injection": ObfuscatedInjectionCase(),
    "indirect_injection": IndirectInjectionCase(),
    "indirect_injection_hidden_metadata": IndirectInjectionHiddenMetadataCase(),
    "indirect_injection_priority_conflict": IndirectInjectionPriorityConflictCase(),
    "indirect_injection_cross_document": IndirectInjectionCrossDocumentCase(),
    "indirect_injection_html_comment": IndirectInjectionHtmlCommentCase(),
    "indirect_injection_quoted_text": IndirectInjectionQuotedTextCase(),
    "indirect_injection_tabular": IndirectInjectionTabularCase(),
    "indirect_injection_dual_task": IndirectInjectionDualTaskCase(),
    "indirect_injection_multi_hop": IndirectInjectionMultiHopCase(),
    "tool_manipulation": ToolManipulationCase(),
    "tool_manipulation_policy_bypass": ToolManipulationPolicyBypassCase(),
    "data_exfiltration_tool_use": DataExfiltrationToolUseCase(),
    "unauthorized_action_execution": UnauthorizedActionExecutionCase(),
    "context_poisoning": ContextPoisoningCase(),
    "persistent_injection": PersistentInjectionCase(),
    "contextual_injection": ContextualInjectionCase(),
    "delayed_trigger_injection": DelayedTriggerInjectionCase(),
}
