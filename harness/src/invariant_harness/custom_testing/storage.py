from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from invariant_harness.custom_testing.types import CustomScenario


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def get_custom_scenarios_dir() -> Path:
    path = _project_root() / "custom_scenarios"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_custom_results_dir() -> Path:
    path = _project_root() / "results" / "custom"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_custom_group_results_dir() -> Path:
    path = _project_root() / "results" / "custom_groups"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_custom_scenario(scenario: CustomScenario) -> Path:
    path = get_custom_scenarios_dir() / f"{scenario.scenario_id}__scenario.json"
    path.write_text(json.dumps(scenario.model_dump(), indent=2), encoding="utf-8")
    return path


def load_custom_scenario(scenario_id: str) -> CustomScenario:
    path = get_custom_scenarios_dir() / f"{scenario_id}__scenario.json"
    return CustomScenario.model_validate_json(path.read_text(encoding="utf-8"))


def delete_custom_scenario(scenario_id: str) -> bool:
    path = get_custom_scenarios_dir() / f"{scenario_id}__scenario.json"
    if not path.exists():
        return False
    path.unlink()
    return True


def list_custom_scenarios() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(get_custom_scenarios_dir().glob("*__scenario.json"), reverse=True):
        scenario = CustomScenario.model_validate_json(path.read_text(encoding="utf-8"))
        items.append(
            {
                "scenario_id": scenario.scenario_id,
                "name": scenario.name,
                "attack_family": scenario.attack_family,
                "mode": scenario.mode,
                "updated_at": scenario.updated_at,
                "tags": scenario.tags,
                "artifact_path": str(path),
            }
        )
    return items


def save_custom_run_artifact(
    payload: dict[str, Any],
    *,
    scenario_name: str,
    provider: str,
    model_name: str,
    timestamp_utc: str,
) -> Path:
    safe_timestamp = timestamp_utc.replace(":", "-")
    filename = f"custom__{scenario_name}__{provider}__{model_name}__{safe_timestamp}.json"
    path = get_custom_results_dir() / filename
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def save_custom_run_group_artifact(
    payload: dict[str, Any],
    *,
    scenario_name: str,
    timestamp_utc: str,
) -> Path:
    safe_timestamp = timestamp_utc.replace(":", "-")
    filename = f"custom_group__{scenario_name}__{safe_timestamp}.json"
    path = get_custom_group_results_dir() / filename
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def list_custom_runs() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(get_custom_results_dir().glob("custom__*.json"), reverse=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["artifact_path"] = str(path)
        items.append(payload)
    return items


def list_custom_run_groups() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(get_custom_group_results_dir().glob("custom_group__*.json"), reverse=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["artifact_path"] = str(path)
        items.append(payload)
    return items


def load_custom_run(artifact_name: str) -> dict[str, Any]:
    path = get_custom_results_dir() / artifact_name
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["artifact_path"] = str(path)
    return payload


def load_custom_run_group(artifact_name: str) -> dict[str, Any]:
    path = get_custom_group_results_dir() / artifact_name
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["artifact_path"] = str(path)
    return payload
