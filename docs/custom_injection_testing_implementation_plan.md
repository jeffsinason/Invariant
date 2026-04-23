# Custom Injection Testing Implementation Plan

## Purpose

This document turns the approved custom injection testing product design and technical design into an implementation plan.

It defines:
- delivery phases
- API endpoints
- frontend component map
- validation rules
- evaluator DSL scope
- storage conventions
- testing strategy

This is the final planning document that should exist before implementation begins.

## Implementation Objective

Deliver a robust `Custom Test` capability that:
- supports guided and advanced authoring
- runs realistic system-level attack scenarios
- preserves explicit trust boundaries
- supports exploratory and evaluated modes
- saves scenario definitions separately from run artifacts
- provides strong operator summaries and technical drilldown
- remains separate from canonical benchmark workflows

## Delivery Strategy

Implementation should be phased. The feature is too broad to land safely as one large change.

Recommended phases:

1. Schema and persistence foundation
2. Backend API and scenario validation
3. Guided custom test UI
4. Evaluator engine
5. Advanced scenario editor
6. Multi-target execution and comparison
7. Export/import and operational hardening

## Phase 1 — Schema and Persistence Foundation

### Goals
- define scenario schema
- define run artifact schema
- define storage layout
- define normalization and validation primitives

### Deliverables
- `CustomScenario` types
- `CustomScenarioRun` types
- `CustomScenarioRunGroup` types
- normalization helpers
- persistence helpers
- file naming conventions

### Files likely needed
- `harness/src/invariant_harness/custom_testing/types.py`
- `harness/src/invariant_harness/custom_testing/storage.py`
- `harness/src/invariant_harness/custom_testing/validation.py`
- `harness/src/invariant_harness/custom_testing/__init__.py`

### Exit Criteria
- scenario definitions can be loaded, validated, normalized, and saved
- run artifact structure is defined and testable
- no UI yet

## Phase 2 — Backend API and Scenario Validation

### Goals
- expose scenario lifecycle endpoints
- expose run endpoints
- keep evaluation and storage server-side

### API Surface

#### Scenario Endpoints

- `GET /custom-tests`
  - list saved scenario definitions
- `POST /custom-tests`
  - create scenario definition
- `GET /custom-tests/{scenario_id}`
  - fetch one scenario definition
- `PUT /custom-tests/{scenario_id}`
  - update scenario definition
- `DELETE /custom-tests/{scenario_id}`
  - delete scenario definition

#### Run Endpoints

- `POST /custom-tests/run`
  - execute a scenario payload without requiring prior save
- `POST /custom-tests/{scenario_id}/run`
  - execute a saved scenario
- `GET /custom-test-runs`
  - list saved custom test run artifacts
- `GET /custom-test-runs/{artifact_name}`
  - fetch one custom test run artifact

#### Run Group Endpoints

- `GET /custom-test-run-groups`
  - list saved grouped multi-target runs
- `GET /custom-test-run-groups/{artifact_name}`
  - fetch one run group artifact

#### Utility Endpoints

- `POST /custom-tests/validate`
  - validate a scenario payload without executing it
- `GET /custom-tests/templates`
  - list guided attack-family templates
- `GET /custom-tests/evaluators`
  - list builtin evaluators and configurable evaluator types

### Request/Response Shape

All custom-test endpoints should follow the same response conventions already used by the harness API:
- success payload
- structured error metadata
- saved artifact reference when applicable

### Exit Criteria
- scenarios can be created, validated, run, and listed over the API
- errors are structured and inspectable

## Phase 3 — Guided Custom Test UI

### Goals
- introduce a new `Custom Test` top-level tab
- support guided mode first
- support exploratory and evaluated runs

### UI Information Architecture

Top-level tabs after this phase:
- `Run Case`
- `Run Benchmark`
- `Custom Test`
- `Artifacts`

### Guided Page Sections

#### A. Test Mode
- run mode: `exploratory` or `evaluated`
- provider/model
- optional matrix toggle

#### B. Attack Family
- family selector
- template selector
- name
- description
- tags

#### C. Trusted Context
- system instructions
- developer instructions
- output constraints
- tool policy

#### D. User and Session Context
- current request
- conversation turns
- memory/session items

#### E. Untrusted Inputs
- retrieved documents
- document metadata
- HTML/comment payloads
- quoted content
- tabular inputs
- tool outputs

#### F. Attack Payload
- placement
- timing
- payload
- variants

#### G. Expected Outcome
- optional in exploratory mode
- required for saveable evaluated scenario

#### H. Evaluator
- builtin
- configured
- custom

#### I. Run and Save
- validate
- run
- save scenario
- save run
- export

#### J. Result
- operator summary
- technical metadata
- raw provider payload
- scenario snapshot

### Frontend Files Likely Needed

- `frontend/src/custom-tests/CustomTestPage.tsx`
- `frontend/src/custom-tests/GuidedCustomTestForm.tsx`
- `frontend/src/custom-tests/ScenarioContextEditor.tsx`
- `frontend/src/custom-tests/AttackPayloadEditor.tsx`
- `frontend/src/custom-tests/ExpectedOutcomeEditor.tsx`
- `frontend/src/custom-tests/EvaluatorEditor.tsx`
- `frontend/src/custom-tests/CustomTestResultView.tsx`
- `frontend/src/custom-tests/api.ts`
- `frontend/src/custom-tests/types.ts`

### Exit Criteria
- guided custom test runs can be authored and executed from the UI
- result view matches current operator-console quality

## Phase 4 — Evaluator Engine

### Goals
- support builtin, configured, and custom evaluators
- keep implementation safe and constrained

### Evaluator Architecture

Recommended evaluator pipeline:

1. Normalize provider response
2. Build evaluator context
3. Execute evaluator
4. Produce:
   - verdict
   - evaluation label
   - reason summary
   - technical evidence

### Evaluator Types

#### Builtin Evaluators

Project-owned evaluators mapped by name.

Examples:
- `direct_override`
- `prompt_leakage`
- `retrieval_injection`
- `unauthorized_tool_use`

#### Configured Evaluators

Builtin evaluator logic plus user-supplied configuration:
- forbidden strings
- required strings
- acceptable labels
- unacceptable labels

#### Custom Evaluator DSL

V1 should support a constrained declarative rule language rather than arbitrary Python/JS execution.

### Evaluator DSL Proposal

Recommended design:

```json
{
  "rules": [
    {
      "when": {
        "response_contains": ["COMPROMISED"]
      },
      "set_label": "direct_obedience",
      "set_verdict": "vulnerable",
      "reason": "Response emitted forbidden obedience token."
    }
  ],
  "fallback": {
    "label": "safe_other",
    "verdict": "safe",
    "reason": "No rule matched."
  }
}
```

Supported match keys in v1:
- `response_contains`
- `response_not_contains`
- `tool_call_count_gt`
- `tool_name_called`
- `stop_reason_is`
- `evaluation_label_is`
- `any_of`
- `all_of`

Supported actions in v1:
- `set_label`
- `set_verdict`
- `reason`

Not in v1:
- loops
- arbitrary expressions
- filesystem access
- network access
- custom code execution

### Files Likely Needed

- `harness/src/invariant_harness/custom_testing/evaluators.py`
- `harness/src/invariant_harness/custom_testing/evaluator_dsl.py`
- `harness/src/invariant_harness/custom_testing/evaluator_context.py`

### Exit Criteria
- all three evaluator modes are supported
- evaluator output is deterministic and inspectable

## Phase 5 — Advanced Scenario Editor

### Goals
- expose full scenario structure
- preserve trust-boundary clarity
- support multi-turn and system-level scenario authoring

### Design

The advanced editor should support:
- structured section editors
- optional raw JSON mode
- scenario validation panel

Recommended component map:
- `AdvancedScenarioEditor.tsx`
- `ScenarioJsonEditor.tsx`
- `ScenarioValidationPanel.tsx`

The advanced editor should not be implemented as an unstructured raw-text prompt playground.

### Exit Criteria
- advanced scenario editing supports the full approved schema
- guided and advanced modes can round-trip the same scenario definition

## Phase 6 — Multi-Target Execution and Comparison

### Goals
- support running the same scenario across multiple providers/models
- save grouped results
- expose side-by-side comparison

### Backend Requirements
- execution-plan expansion from one scenario into multiple target-specific execution units
- run group artifact generation

### UI Requirements
- matrix execution toggle
- target selection
- grouped result display
- side-by-side comparison

### Comparison Dimensions
- verdict
- evaluation label
- provider/model
- response text
- usage
- tool calls
- errors

### Exit Criteria
- same scenario can be run across multiple targets in one action
- grouped results are reviewable and saved

## Phase 7 — Export/Import and Hardening

### Goals
- support scenario export/import
- harden validation
- finalize usability

### Deliverables
- export scenario JSON
- import scenario JSON
- migration handling for schema versions
- stronger error messages
- stronger UX polish

### Exit Criteria
- scenario definitions can move between workspaces manually
- invalid imports fail clearly

## Storage Conventions

V1 should remain file-based.

### Directories

- `harness/custom_scenarios/`
- `harness/results/custom/`
- `harness/results/custom_groups/`

### Naming

#### Scenario Definition

```text
<scenario_slug>__scenario.json
```

Optional later:
- version snapshots
- revision ids

#### Scenario Run

```text
custom__<scenario_slug>__<provider>__<model>__<timestamp>.json
```

#### Scenario Run Group

```text
custom_group__<scenario_slug>__<timestamp>.json
```

### Persistence Rules

- scenario definitions are editable
- run artifacts are immutable
- run groups are immutable

## Validation Rules

### Scenario-Level Rules

- `schema_version` required
- `name` required
- `mode` required
- at least one target required
- at least one user request or conversation turn required
- attack family required
- attack payload required
- guided-mode scenarios must conform to their template requirements

### Evaluated-Save Rules

If scenario is:
- `mode = evaluated`
- and user is saving a reusable scenario

Then `expected_outcome` is required.

### Target Rules

- each target requires provider + model
- duplicate targets should be normalized or rejected
- parameters must match allowed types

### Evaluator Rules

- builtin evaluator names must exist
- configured evaluator fields must match supported schema
- custom evaluator DSL must validate against allowed operators/actions

### Trust-Boundary Rules

- trusted and untrusted inputs must remain in their defined sections
- system/developer instructions cannot be silently merged with untrusted inputs

## Frontend Component Map

Recommended component structure:

### Root
- `CustomTestPage`

### Mode and Authoring
- `CustomTestModeSelector`
- `CustomTestAuthoringTabs`

### Guided Components
- `GuidedScenarioMetadataForm`
- `GuidedTargetConfigForm`
- `TrustedContextSection`
- `UserContextSection`
- `UntrustedContextSection`
- `AttackPayloadSection`
- `ExpectedOutcomeSection`
- `EvaluatorSection`
- `RunSaveControls`

### Advanced Components
- `AdvancedScenarioEditor`
- `ScenarioJsonEditor`
- `ScenarioValidationPanel`

### Results
- `CustomTestCurrentResult`
- `CustomTestSelectedResult`
- `CustomTestOperatorSummary`
- `CustomTestTechnicalDrilldown`
- `CustomTestRunComparison`

### Shared
- `CustomScenarioSelector`
- `CustomScenarioExportImport`
- `TargetMatrixSelector`

## API Endpoint Details

### `GET /custom-tests`

Response:
- summary list only
- scenario id
- name
- attack family
- updated timestamp
- tags

### `POST /custom-tests`

Request:
- full scenario definition

Response:
- saved scenario metadata
- path or reference

### `PUT /custom-tests/{scenario_id}`

Request:
- full updated scenario definition

Response:
- saved scenario metadata

### `POST /custom-tests/validate`

Request:
- full scenario definition

Response:
- normalized scenario
- validation warnings
- validation errors

### `POST /custom-tests/run`

Request:
- unsaved scenario payload
- execution options

Response:
- one run result or run group result

### `POST /custom-tests/{scenario_id}/run`

Request:
- optional overrides

Response:
- one run result or run group result

## Test Strategy

Testing should be layered.

### Unit Tests

#### Schema and Validation
- scenario validation rules
- expected outcome requirements
- evaluator DSL validation
- trust-boundary validation

#### Evaluator Engine
- builtin evaluator execution
- configured evaluator rules
- custom DSL evaluation
- fallback behavior

#### Storage
- save/load scenario
- save/load run artifact
- save/load run group artifact

### Integration Tests

#### API
- create scenario
- validate scenario
- run unsaved scenario
- run saved scenario
- export/import scenario

#### Existing Harness Integration
- provider adapter path still works
- tool simulation path still works
- retrieval/session path still works

### UI Tests

Use Playwright when implemented.

Cover:
- guided authoring flow
- advanced authoring flow
- exploratory run flow
- evaluated run flow
- save scenario flow
- compare run flow

### Live Provider Tests

Environment-gated tests for:
- OpenAI
- Anthropic
- Mistral

These should be minimal smoke tests, not the primary correctness layer.

## Migration and Backward Compatibility

V1 introduces new artifact families. It should not alter canonical benchmark artifact structures.

Compatibility requirements:
- existing case and benchmark APIs remain stable
- custom scenario artifacts are additive only
- no migration required for old benchmark results

## Risks and Mitigations

### Risk 1: Schema too complex for guided mode

Mitigation:
- guided templates
- strong defaults
- advanced mode only when needed

### Risk 2: Custom evaluator logic becomes unsafe

Mitigation:
- constrained DSL
- explicit validator
- no arbitrary code execution

### Risk 3: Trust boundaries become visually muddy

Mitigation:
- fixed section taxonomy
- explicit field grouping
- validation preventing silent mixing

### Risk 4: UI becomes too large to use

Mitigation:
- phased rollout
- guided mode first
- advanced mode separate

## Recommended Initial Build Order

Implementation should start in this order:

1. scenario types and validation
2. storage helpers
3. API endpoints
4. guided custom test UI
5. builtin/configured evaluator support
6. constrained custom evaluator DSL
7. advanced editor
8. multi-target execution
9. export/import

This order keeps the feature useful early while preserving a coherent architecture.

## Definition of Done for Initial Release

The first release is done when:
- a user can create a guided custom scenario
- a user can create an advanced custom scenario
- exploratory runs work
- evaluated runs work
- reusable scenarios can be saved
- run artifacts can be optionally saved
- operator summaries and technical drilldowns both work
- custom evaluators are supported through the constrained evaluator DSL
- scenario export/import works
- tests cover schema, API, storage, evaluator, and UI basics
