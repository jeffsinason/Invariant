from __future__ import annotations

import re
from typing import Any

from invariant_harness.custom_testing.types import CustomScenario

ALLOWED_ATTACK_PLACEMENTS = {
    "system_prompt",
    "developer_prompt",
    "user_message",
    "retrieved_document",
    "document_metadata",
    "html_comment",
    "quoted_text",
    "table_cell",
    "tool_output",
    "memory_item",
    "conversation_turn",
}

ALLOWED_ATTACK_TIMINGS = {"immediate", "delayed", "multi_turn", "multi_hop"}
ALLOWED_EVALUATOR_MATCH_KEYS = {
    "response_contains",
    "response_not_contains",
    "tool_call_count_gt",
    "tool_name_called",
    "stop_reason_is",
    "evaluation_label_is",
    "any_of",
    "all_of",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "custom-scenario"


def normalize_custom_scenario(scenario: CustomScenario) -> CustomScenario:
    normalized = scenario.model_copy(deep=True)

    normalized.name = normalized.name.strip()
    normalized.description = normalized.description.strip()
    normalized.attack_family = normalized.attack_family.strip()
    normalized.tags = sorted({tag.strip() for tag in normalized.tags if tag.strip()})
    normalized.updated_at = normalized.updated_at

    if not normalized.target_config.default_provider and normalized.target_config.targets:
        normalized.target_config.default_provider = normalized.target_config.targets[0].provider
    if not normalized.target_config.default_model and normalized.target_config.targets:
        normalized.target_config.default_model = normalized.target_config.targets[0].model

    if not normalized.scenario_id:
        normalized.scenario_id = slugify(normalized.name)

    return normalized


def validate_custom_scenario(
    scenario: CustomScenario,
    *,
    for_save: bool = False,
) -> tuple[CustomScenario, list[str]]:
    normalized = normalize_custom_scenario(scenario)
    warnings: list[str] = []

    if not normalized.name:
        raise ValueError("Scenario name is required")
    if not normalized.attack_family:
        raise ValueError("Attack family is required")
    if not normalized.target_config.targets:
        raise ValueError("At least one target is required")
    if (
        not normalized.context.user.current_request.strip()
        and not normalized.context.user.conversation_turns
    ):
        raise ValueError("A current request or conversation turn is required")
    if not normalized.attack.payload.strip():
        raise ValueError("Attack payload is required")
    if normalized.attack.placement not in ALLOWED_ATTACK_PLACEMENTS:
        raise ValueError(f"Unsupported attack placement: {normalized.attack.placement}")
    if normalized.attack.timing not in ALLOWED_ATTACK_TIMINGS:
        raise ValueError(f"Unsupported attack timing: {normalized.attack.timing}")

    seen_targets: set[tuple[str, str]] = set()
    for target in normalized.target_config.targets:
        key = (target.provider.strip(), target.model.strip())
        if not all(key):
            raise ValueError("Each target requires both provider and model")
        if key in seen_targets:
            raise ValueError("Duplicate targets are not allowed")
        seen_targets.add(key)

    if (
        for_save
        and normalized.mode == "evaluated"
        and not _has_expected_outcome(normalized.expected_outcome)
    ):
        raise ValueError(
            "Expected outcome is required to save a reusable evaluated custom scenario"
        )

    if normalized.evaluator.type == "builtin" and not normalized.evaluator.builtin_name:
        warnings.append("Builtin evaluator selected without builtin_name; generic evaluation will be used.")

    if normalized.evaluator.type == "custom":
        _validate_custom_logic(normalized.evaluator.custom_logic)

    if not normalized.context.untrusted.retrieved_documents and normalized.attack.placement in {
        "retrieved_document",
        "document_metadata",
        "html_comment",
        "quoted_text",
        "table_cell",
    }:
        warnings.append(
            "Attack placement targets untrusted retrieved content, but no retrieved documents were supplied."
        )

    return normalized, warnings


def _has_expected_outcome(expected_outcome: Any) -> bool:
    if not expected_outcome:
        return False
    return any(
        [
            bool(expected_outcome.behavior_category),
            bool(expected_outcome.forbidden_outputs),
            bool(expected_outcome.required_outputs),
            bool(expected_outcome.acceptable_labels),
            bool(expected_outcome.unacceptable_labels),
        ]
    )


def _validate_custom_logic(custom_logic: dict[str, Any]) -> None:
    if not custom_logic:
        raise ValueError("Custom evaluator selected without custom logic")
    rules = custom_logic.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("Custom evaluator rules must be a list")
    for rule in rules:
        when = rule.get("when", {})
        if not isinstance(when, dict):
            raise ValueError("Custom evaluator rule 'when' must be an object")
        for key in when:
            if key not in ALLOWED_EVALUATOR_MATCH_KEYS:
                raise ValueError(f"Unsupported custom evaluator condition: {key}")
