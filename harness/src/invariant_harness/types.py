from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from typing import Any


@dataclass
class Prompt:
    system: str
    user: str


@dataclass
class RetrievedContent:
    source: str
    content: str
    trust_level: str = "untrusted"


@dataclass
class ToolSpec:
    name: str
    description: str
    allowed: bool = True


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class ConversationTurn:
    role: str
    content: str


@dataclass
class SessionMemory:
    key: str
    value: str


@dataclass
class ModelResponse:
    output: str
    provider: str
    model_name: str
    raw: Any | None = None
    request_id: str | None = None
    stop_reason: str | None = None
    usage: dict[str, Any] | None = None
    tool_calls: list[ToolCall] | None = None


@dataclass
class CaseResult:
    case_name: str
    provider: str
    model_name: str
    vulnerable: bool
    response_text: str
    evaluation_label: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    notes: str = ""
    raw_response: Any | None = None
    request_id: str | None = None
    stop_reason: str | None = None
    usage: dict[str, Any] | None = None
    tool_calls: list[ToolCall] | None = None
    timestamp_utc: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp_utc:
            self.timestamp_utc = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
