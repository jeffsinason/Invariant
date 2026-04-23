from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class ScenarioTarget(BaseModel):
    provider: str
    model: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class TargetConfig(BaseModel):
    default_provider: str | None = None
    default_model: str | None = None
    targets: list[ScenarioTarget] = Field(default_factory=list)


class TrustedContext(BaseModel):
    system_instructions: str = ""
    developer_instructions: str | None = None
    output_constraints: list[str] = Field(default_factory=list)
    tool_policy: dict[str, Any] = Field(default_factory=dict)


class ConversationTurnInput(BaseModel):
    role: str
    content: str


class UserContext(BaseModel):
    current_request: str = ""
    conversation_turns: list[ConversationTurnInput] = Field(default_factory=list)


class RetrievedDocument(BaseModel):
    document_id: str | None = None
    title: str = ""
    content_type: str = "plain_text"
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolOutput(BaseModel):
    tool_name: str
    content: str
    content_type: str = "plain_text"


class UntrustedContext(BaseModel):
    retrieved_documents: list[RetrievedDocument] = Field(default_factory=list)
    tool_outputs: list[ToolOutput] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class MemoryItem(BaseModel):
    memory_id: str | None = None
    content: str
    source: str = "external"
    trust_level: str = "untrusted"


class MemoryContext(BaseModel):
    session_summary: str | None = None
    memory_items: list[MemoryItem] = Field(default_factory=list)


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters_schema: dict[str, Any] = Field(default_factory=dict)
    authorization: dict[str, Any] = Field(default_factory=dict)


class ToolsContext(BaseModel):
    available_tools: list[ToolDefinition] = Field(default_factory=list)


class ScenarioContext(BaseModel):
    trusted: TrustedContext = Field(default_factory=TrustedContext)
    user: UserContext = Field(default_factory=UserContext)
    untrusted: UntrustedContext = Field(default_factory=UntrustedContext)
    memory: MemoryContext = Field(default_factory=MemoryContext)
    tools: ToolsContext = Field(default_factory=ToolsContext)


class AttackVariant(BaseModel):
    variant_id: str | None = None
    label: str
    payload_override: str | None = None
    placement_override: str | None = None
    timing_override: str | None = None


class AttackSpec(BaseModel):
    family: str
    template: str | None = None
    placement: str = "retrieved_document"
    timing: str = "immediate"
    payload: str
    objective: str | None = None
    variants: list[AttackVariant] = Field(default_factory=list)


class ExpectedOutcome(BaseModel):
    required: bool = False
    behavior_category: str | None = None
    forbidden_outputs: list[str] = Field(default_factory=list)
    required_outputs: list[str] = Field(default_factory=list)
    acceptable_labels: list[str] = Field(default_factory=list)
    unacceptable_labels: list[str] = Field(default_factory=list)


class EvaluatorSpec(BaseModel):
    type: Literal["builtin", "configured", "custom"] = "builtin"
    builtin_name: str | None = None
    configured_rules: dict[str, Any] = Field(default_factory=dict)
    custom_logic: dict[str, Any] = Field(default_factory=dict)


class SavePreferences(BaseModel):
    save_scenario_by_default: bool = True
    save_run_by_default: bool = False


class CustomScenario(BaseModel):
    schema_version: str = "1.0"
    scenario_id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    description: str = ""
    mode: Literal["exploratory", "evaluated"] = "exploratory"
    authoring_mode: Literal["guided", "advanced"] = "guided"
    attack_family: str
    tags: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)
    target_config: TargetConfig
    context: ScenarioContext
    attack: AttackSpec
    expected_outcome: ExpectedOutcome | None = None
    evaluator: EvaluatorSpec = Field(default_factory=EvaluatorSpec)
    save_preferences: SavePreferences = Field(default_factory=SavePreferences)


class ValidationRequest(BaseModel):
    scenario: CustomScenario
    for_save: bool = False


class CustomScenarioRunRequest(BaseModel):
    scenario: CustomScenario
    save_run: bool = False


class SavedCustomScenarioRunRequest(BaseModel):
    save_run: bool = False

