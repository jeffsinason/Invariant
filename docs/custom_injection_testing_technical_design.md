# Custom Injection Testing Technical Design

## Purpose

This document translates the approved product design for custom injection testing into a technical design that can guide implementation.

It covers:
- scenario schema
- UI information architecture
- evaluator architecture
- storage model
- execution flow
- safeguards and non-goals

This document does not authorize implementation by itself. It defines the structure that implementation should follow.

## Design Constraints

The technical design must preserve these product decisions:

- custom tests are separate from canonical benchmarks
- realistic system-level attack scenarios are the default
- both guided and advanced authoring modes exist in v1
- prompt/context/retrieval/tools/memory are included in v1
- one provider/model at a time is the default execution mode
- multi-provider/model execution is supported but secondary
- expected outcome is optional for exploratory runs and required for reusable saved scenarios
- exploratory runs should still be classified when possible
- full custom evaluator logic is allowed at the product level, but implementation must use a safe constrained model
- custom tests live in a dedicated `Custom Test` top-level tab

## System Overview

Custom injection testing should be implemented as a new scenario-driven layer on top of the existing harness rather than as a separate execution system.

High-level stack:

1. `CustomScenario` definition
2. scenario validation and normalization
3. scenario execution planning
4. provider/model execution via existing adapters
5. custom evaluation
6. result persistence
7. UI drilldown and comparison

This keeps one execution core for:
- providers
- result artifacts
- evaluation metadata
- storage patterns

## Core Entities

The feature requires four primary persisted concepts.

### 1. CustomScenario

The reusable scenario definition authored by the user.

Properties:
- editable
- exportable
- importable
- versionable

### 2. CustomScenarioRun

One execution of a scenario against one provider/model target.

Properties:
- immutable once saved
- tied to a scenario snapshot
- contains raw provider result and evaluator output

### 3. CustomScenarioRunGroup

A logical grouping of multiple target runs for the same scenario execution request.

Used when the user runs a scenario against:
- multiple models
- multiple providers

Properties:
- one group
- many run artifacts

### 4. CustomEvaluatorDefinition

The evaluation configuration attached to a scenario.

This can be:
- project-provided evaluator selection
- configured rule set
- constrained custom evaluator expression

## Scenario Schema

The schema should be explicit, portable, and inspectable as JSON or YAML.

Recommended top-level structure:

```json
{
  "schema_version": "1.0",
  "scenario_id": "uuid-or-slug",
  "name": "string",
  "description": "string",
  "mode": "exploratory | evaluated",
  "authoring_mode": "guided | advanced",
  "attack_family": "string",
  "tags": ["string"],
  "created_at": "iso8601",
  "updated_at": "iso8601",
  "target_config": {},
  "context": {},
  "attack": {},
  "expected_outcome": {},
  "evaluator": {},
  "save_preferences": {}
}
```

### Schema Versioning

`schema_version` is required.

Reason:
- export/import stability
- future migration support
- compatibility checks

## Target Configuration Schema

This defines where the scenario runs.

```json
{
  "default_provider": "openai",
  "default_model": "gpt-4.1-mini",
  "targets": [
    {
      "provider": "openai",
      "model": "gpt-4.1-mini",
      "parameters": {
        "temperature": 0.2,
        "max_tokens": 512
      }
    }
  ]
}
```

Rules:
- at least one target required
- exactly one target is the default UI path
- multiple targets allowed for comparison runs

The UI should treat `targets[0]` as the default execution target unless the user explicitly enables matrix execution.

## Context Schema

The context model must preserve trust boundaries explicitly.

```json
{
  "trusted": {
    "system_instructions": "string",
    "developer_instructions": "string | null",
    "output_constraints": ["string"],
    "tool_policy": {}
  },
  "user": {
    "current_request": "string",
    "conversation_turns": []
  },
  "untrusted": {
    "retrieved_documents": [],
    "tool_outputs": [],
    "notes": []
  },
  "memory": {
    "session_summary": "string | null",
    "memory_items": []
  },
  "tools": {
    "available_tools": []
  }
}
```

### Trusted Context

Fields:
- `system_instructions`
- `developer_instructions`
- `output_constraints`
- `tool_policy`

### User Context

Fields:
- `current_request`
- `conversation_turns`

Each `conversation_turn`:

```json
{
  "role": "user | assistant",
  "content": "string"
}
```

### Untrusted Retrieved Documents

Each document:

```json
{
  "document_id": "string",
  "title": "string",
  "content_type": "plain_text | html | markdown | csv | json | metadata",
  "content": "string",
  "metadata": {
    "source": "string",
    "notes": "string"
  }
}
```

### Untrusted Tool Outputs

Each tool output:

```json
{
  "tool_name": "string",
  "content": "string",
  "content_type": "plain_text | json | html"
}
```

### Memory

Memory is separate from retrieved documents because it participates differently in trust and persistence.

Each memory item:

```json
{
  "memory_id": "string",
  "content": "string",
  "source": "system | assistant | external",
  "trust_level": "trusted | untrusted"
}
```

### Tools

Each tool definition:

```json
{
  "name": "string",
  "description": "string",
  "parameters_schema": {},
  "authorization": {
    "allowed": true,
    "scope": "string",
    "conditions": ["string"]
  }
}
```

## Attack Schema

The attack must be represented directly rather than inferred from free-form text alone.

```json
{
  "family": "indirect_injection",
  "template": "priority_conflict",
  "placement": "retrieved_document",
  "timing": "immediate",
  "payload": "string",
  "objective": "string",
  "variants": []
}
```

### Placement

Allowed placements:
- `system_prompt`
- `developer_prompt`
- `user_message`
- `retrieved_document`
- `document_metadata`
- `html_comment`
- `quoted_text`
- `table_cell`
- `tool_output`
- `memory_item`
- `conversation_turn`

### Timing

Allowed timing:
- `immediate`
- `delayed`
- `multi_turn`
- `multi_hop`

### Variants

Variants support repeated related attack attempts within one scenario definition.

Each variant:

```json
{
  "variant_id": "string",
  "label": "string",
  "payload_override": "string | null",
  "placement_override": "string | null",
  "timing_override": "string | null"
}
```

This is useful for:
- slight attack variations
- repeated phrasing tests
- minor formatting changes

## Expected Outcome Schema

Expected outcome is optional in exploratory mode and required for saveable evaluated scenarios.

```json
{
  "required": false,
  "behavior_category": "ignore_untrusted_instruction",
  "forbidden_outputs": ["COMPROMISED"],
  "required_outputs": [],
  "acceptable_labels": ["safe_summary", "safe_refusal"],
  "unacceptable_labels": ["direct_obedience"]
}
```

Validation rules:
- exploratory mode may omit `expected_outcome`
- evaluated scenarios intended for save must include it

## Evaluator Schema

Three evaluator types should exist in the schema.

```json
{
  "type": "builtin | configured | custom",
  "builtin_name": "retrieval_injection",
  "configured_rules": {},
  "custom_logic": {}
}
```

### Builtin

Uses a project-owned evaluator by name.

Example:

```json
{
  "type": "builtin",
  "builtin_name": "prompt_leakage"
}
```

### Configured

Uses project-supported evaluator templates plus user configuration.

Example:

```json
{
  "type": "configured",
  "configured_rules": {
    "forbidden_outputs": ["COMPROMISED"],
    "acceptable_labels": ["safe_summary", "safe_refusal"]
  }
}
```

### Custom

Uses constrained custom evaluator logic.

This should **not** be implemented as arbitrary Python or JavaScript execution in v1.

Recommended v1 design:
- a constrained expression language or declarative rule DSL
- no unrestricted code execution
- no filesystem or network access from evaluator logic

Example conceptual shape:

```json
{
  "type": "custom",
  "custom_logic": {
    "rules": [
      {
        "if": "response.contains('COMPROMISED')",
        "label": "direct_obedience",
        "verdict": "vulnerable"
      }
    ],
    "fallback_label": "safe_other",
    "fallback_verdict": "safe"
  }
}
```

This satisfies the product requirement for custom evaluator logic while staying technically defensible.

## Scenario File Format

Recommended file format:
- JSON for API and storage
- optional YAML import/export for user-facing portability later

V1 recommendation:
- persist canonical format as JSON
- export/import JSON first
- leave YAML for later unless it becomes a clear user demand

## UI Information Architecture

The `Custom Test` tab should have two submodes:
- `Guided`
- `Advanced`

## Guided UI Structure

Recommended page structure:

### Section 1: Test Mode
- `exploratory` or `evaluated`
- target provider/model
- optional matrix toggle

### Section 2: Attack Family
- family selector
- template selector
- tags

### Section 3: Trusted Context
- system instructions
- developer instructions
- output constraints
- tool policy

### Section 4: User and Session Context
- current request
- conversation turns
- memory/session inputs

### Section 5: Untrusted Inputs
- retrieved documents
- metadata
- HTML/comments
- quoted content
- tables/CSV
- tool outputs

### Section 6: Attack Payload
- placement
- timing
- payload
- variants

### Section 7: Expected Outcome
- behavior category
- forbidden outputs
- required outputs
- acceptable/unacceptable labels

### Section 8: Evaluator
- builtin/configured/custom
- evaluator-specific controls

### Section 9: Run and Save
- run
- save scenario
- save run
- export

### Section 10: Results
- operator summary
- technical drilldown
- raw payloads

## Advanced UI Structure

Advanced mode should expose the scenario explicitly.

Recommended layout:

### Left panel
- scenario metadata
- structured editor sections
- evaluator editor

### Right panel
- validation panel
- execution controls
- result drilldown

Advanced mode should still preserve structured editing rather than collapsing everything into one raw text blob.

Recommended representation:
- form sections for major objects
- optional raw JSON editor toggle for the full scenario definition

This allows:
- technical control
- schema transparency
- easier debugging

## Validation Model

Validation should happen in three stages.

### 1. Authoring Validation

Before run:
- required fields
- incompatible combinations
- malformed targets
- malformed tool definitions
- malformed evaluator definitions

### 2. Execution Validation

Before provider call:
- normalized scenario structure
- valid execution plan
- safe evaluator configuration

### 3. Persistence Validation

Before save:
- expected outcome present when saving reusable evaluated scenario
- exportable JSON shape valid

## Execution Flow

Recommended execution pipeline:

1. load scenario from UI
2. normalize and validate scenario
3. expand targets and variants into execution units
4. build execution context from trusted/user/untrusted/memory/tool inputs
5. map execution unit into existing harness primitives
6. invoke provider/model adapter
7. classify response with builtin/configured/custom evaluator
8. generate operator summary and technical result
9. optionally save run artifact
10. optionally keep or save scenario definition

### Execution Unit

Each execution unit should contain:
- scenario snapshot
- target
- variant
- evaluator snapshot

This makes later result analysis cleaner and reproducible.

## Mapping to Existing Harness

Custom testing should reuse the existing harness wherever possible.

Reuse targets:
- provider loading
- model adapters
- response metadata capture
- result persistence model
- tool simulation where applicable
- retrieval/session utilities where applicable

New additions needed:
- scenario normalization layer
- custom scenario runner
- evaluator engine for custom scenarios
- scenario persistence layer

## Storage Model

V1 can remain file-based, consistent with the rest of the harness.

Recommended directories:

- `harness/custom_scenarios/`
- `harness/results/custom/`

### Scenario files

Suggested naming:

```text
<scenario_name>__<timestamp>.json
```

Better long-term:
- stable scenario id
- latest editable scenario file
- optional version snapshots

### Run artifacts

Suggested naming:

```text
custom__<scenario_name>__<provider>__<model>__<timestamp>.json
```

### Run group artifacts

When one scenario is executed against multiple targets:

```text
custom_group__<scenario_name>__<timestamp>.json
```

This group artifact should reference the child run artifacts.

## Result Schema

Each custom scenario run should include:

```json
{
  "artifact_type": "custom_scenario_run",
  "scenario_id": "string",
  "scenario_name": "string",
  "scenario_mode": "exploratory | evaluated",
  "attack_family": "string",
  "provider": "string",
  "model_name": "string",
  "variant_id": "string | null",
  "verdict": "safe | vulnerable | error",
  "evaluation_label": "string | null",
  "response_text": "string",
  "notes": "string",
  "request_id": "string | null",
  "stop_reason": "string | null",
  "usage": {},
  "tool_calls": [],
  "raw_response": {},
  "expected_outcome": {},
  "evaluator_snapshot": {},
  "scenario_snapshot": {},
  "timestamp_utc": "iso8601"
}
```

The inclusion of `scenario_snapshot` is important. Runs should remain reproducible even if the source scenario is later edited.

## Comparison Model

Custom scenario comparison should operate at three levels:

### 1. Single scenario, multiple targets
- compare the same scenario across providers/models

### 2. Same scenario over time
- compare reruns of the same scenario against the same provider/model

### 3. Similar scenarios
- compare related scenario variants

This should remain separate from canonical benchmark comparison in terminology and storage.

## Security and Safety Safeguards

### 1. No arbitrary code execution in evaluators

Even though the product requirement allows “full custom evaluator logic,” v1 should implement this using a constrained DSL or safe evaluator language.

### 2. No raw HTML rendering

All scenario content and results must render as plain text unless explicitly sanitized for a known-safe structured view.

### 3. Tool simulation before real execution

If tool-backed custom testing expands later, tool behavior should remain simulated by default.

### 4. Strong trust-boundary labeling

The UI and schema must never blur trusted instructions with untrusted content.

## Non-Goals for V1

V1 should not include:
- arbitrary scripting hooks with full runtime power
- collaborative shared scenario libraries
- automatic promotion of custom scenarios into canonical benchmark suites
- cloud-hosted scenario syncing
- enterprise role-based access controls

## Recommended Implementation Order

### Phase 1: Scenario Schema and Validation
- define `CustomScenario`
- define validation rules
- define storage shape

### Phase 2: Guided Authoring UI
- build guided form sections
- support exploratory single-target runs

### Phase 3: Evaluator Engine
- builtin
- configured
- constrained custom evaluator DSL

### Phase 4: Advanced Editor
- structured advanced scenario editing
- raw JSON view if needed

### Phase 5: Multi-Target Execution and Comparison
- run groups
- compare results across providers/models

### Phase 6: Export/Import
- scenario import/export
- version handling

## Implementation Readiness Questions

Before coding starts, these still need explicit decisions:

1. JSON only, or JSON plus YAML in v1?
2. What constrained evaluator DSL is acceptable?
3. How much matrix execution belongs in v1 versus later?
4. What exact directory and naming strategy should be used for scenario persistence?
5. Should scenario editing support explicit version history in v1?

## Recommended Next Step

The next document should be implementation planning:
- API endpoints
- frontend component map
- scenario validation rules
- evaluator DSL proposal
- persistence conventions
- migration/testing strategy
