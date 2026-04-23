# Custom Injection Testing Design

## Purpose

This document defines the product and design direction for custom injection testing in Invariant before implementation begins.

The intent is to make custom injection testing a first-class capability of the platform, not a minor extension of canonical case execution. It should become one of the primary reasons to use the harness:
- fast exploratory attack testing
- structured scenario testing
- provider/model comparison
- rigorous artifact capture
- technical drilldown for analysts

This feature must support both operator usability and research rigor.

## Product Position

Custom injection testing is distinct from canonical case execution.

- **Canonical cases** are controlled, project-owned, hardened over time, and suitable for official benchmark workflows.
- **Custom tests** are user-authored attack scenarios intended for exploration, reproduction of field findings, provider comparison, and internal security testing.

Saved custom tests should remain separate from canonical benchmarks. The canonical benchmark suite is expected to stay curated and controlled by the project over time.

## Design Decisions Captured

The following decisions were made before design finalization:

1. Custom testing should support both:
   - single-shot prompt experiments
   - realistic system-level attack scenarios

   Default: **realistic system-level attack scenarios**

2. Expected outcome should be:
   - optional for exploratory runs
   - required to save as a reusable scenario

3. First version should include both:
   - guided templates
   - advanced scenario editor

4. Saved custom tests should **not** become part of canonical benchmark workflows.

5. First version should include:
   - prompt/context
   - retrieval
   - tools
   - memory/session

6. Custom testing should support both:
   - one provider/model at a time
   - multiple providers/models in one run

   Default: **one provider/model at a time**

7. Saving behavior:
   - save the scenario definition only unless the user explicitly saves the run result

8. First version should support:
   - full custom evaluator logic

9. UI placement:
   - its own top-level tab: **`Custom Test`**

10. Primary audience:
   - technical security researchers
   - product/security operators

   Target: **both equally**

11. System instructions:
   - both free-form and structured/template-driven input should exist
   - structured mode should be the default

12. Multi-turn support:
   - both guided and advanced modes should support multi-turn testing

13. Run modes:
   - both `exploratory` and `evaluated`

14. Exploratory runs should still be internally classified when possible.

15. Sharing/reuse in first version:
   - export/import scenario files manually
   - possible future expansion to built-in shared libraries

## Feature Definition

Custom injection testing is:

> A structured interface for designing, running, saving, comparing, and drilling into custom prompt-injection and AI security attack scenarios across providers and models.

The feature must support two parallel workflows:

### 1. Exploratory Workflow

Use case:
- operator wants to try an attack quickly
- no formal saved scenario required
- result should still be classified and recorded if possible

Properties:
- low friction
- immediate execution
- optional expected outcome
- optional saved run artifact

### 2. Evaluated Scenario Workflow

Use case:
- researcher wants a reusable, rigorous scenario
- scenario should be rerunnable and comparable
- expected behavior must be explicit

Properties:
- structured scenario definition
- explicit expected outcome
- saveable scenario definition
- optional saved run artifact
- suitable for technical review and later reuse

## Scope of the First Version

Version 1 should support:
- guided custom test builder
- advanced scenario editor
- one-model execution by default
- optional multi-model/provider execution
- prompt/context/retrieval/tools/memory
- exploratory and evaluated modes
- structured scenario save/load
- run artifact save/load
- export/import of scenario definitions
- project-provided and fully custom evaluator logic
- classification of responses even in exploratory mode when possible

Version 1 should not attempt:
- canonical benchmark integration for custom scenarios
- shared cloud-hosted scenario libraries
- collaborative permissions/workflow systems
- arbitrary scripting execution on the server

## UX Structure

Custom testing should live in its own top-level tab:

- `Run Case`
- `Run Benchmark`
- `Custom Test`
- `Artifacts`

This is necessary because custom testing is its own workflow and should not be buried under `Run Case`.

## Interaction Model

The `Custom Test` tab should support two submodes:

### Guided Mode

This is the default mode.

Goal:
- make robust system-level attack testing accessible without requiring direct schema editing

Sections:
1. Target
2. Test Mode
3. Scenario Context
4. Attack Payload
5. Expected Outcome
6. Evaluator
7. Run Controls
8. Result and Drilldown

### Advanced Mode

Goal:
- let technical users define the full scenario precisely

Sections:
1. Metadata
2. Structured scenario editor
3. Evaluator editor
4. Execution controls
5. Result and drilldown

The advanced editor should expose the full scenario structure explicitly rather than hiding it behind simplified UI controls.

## Core Scenario Model

The feature should be built around a reusable scenario definition rather than raw form state.

At minimum, a `CustomScenario` should contain:

### A. Metadata
- scenario name
- description
- author or local owner
- tags
- attack family
- created timestamp
- updated timestamp
- mode (`exploratory` or `evaluated`)

### B. Target Configuration
- provider
- model
- optional provider/model matrix
- temperature
- max tokens
- additional model parameters when needed

### C. Trusted Context
- system instructions
- developer instructions if modeled separately
- tool authorization policy
- output constraints

### D. User Context
- user request
- conversation turns
- memory/session history

### E. Untrusted Context
- retrieved documents
- document metadata
- quoted material
- HTML/comment payloads
- table/CSV payloads
- tool outputs
- external reference chain / multi-hop content

### F. Attack Payload
- attack family
- attack text
- attack placement
- attack timing
- attack objective

### G. Expected Outcome
- optional in exploratory runs
- required for saved reusable scenarios

Possible components:
- expected behavior category
- forbidden outputs
- required outputs
- acceptable labels
- unacceptable labels

### H. Evaluator Definition
- project-provided evaluator selection
- evaluator configuration
- full custom evaluator logic

### I. Persistence Preferences
- save scenario definition
- save run artifact
- export path or export intent

## Guided Mode Inputs

Guided mode should not be a blank editor. It should be template-driven.

### Recommended attack-family templates

- Direct instruction override
- Prompt leakage
- Indirect retrieved-content injection
- HTML/comment injection
- Metadata injection
- Cross-document poisoning
- Multi-hop retrieval injection
- Dual-task bait
- Role confusion
- Context poisoning
- Persistent injection
- Tool manipulation
- Unauthorized action execution
- Data exfiltration attempt

Each template should pre-structure the relevant fields:
- trusted instructions
- user task
- untrusted content
- attack insertion point
- evaluator defaults

This avoids malformed tests and keeps the feature usable for non-authors of the underlying schema.

## Advanced Mode Inputs

Advanced mode should allow explicit editing of:
- system/developer/user messages
- retrieval fixtures
- tool definitions
- memory/session turns
- authorization policy
- evaluator logic

This mode should make the trust boundary explicit rather than flattening all text into one textarea.

## Trust-Boundary Presentation

This feature depends on trust-boundary clarity.

The UI must visually and semantically separate:
- trusted instructions
- user request
- untrusted retrieved content
- memory/history
- tool specifications
- tool outputs

If these boundaries are unclear in the UI, the feature becomes conceptually weak and the results become hard to defend.

## Execution Parameters

Custom testing should support both:
- one provider/model by default
- optional provider/model matrix execution

The default should remain:
- one provider/model at a time

This keeps the base workflow focused, while still allowing later comparison runs using the same scenario.

Execution controls should include:
- provider
- model
- optional multi-target expansion
- save run artifact toggle
- run button
- rerun button

Advanced controls can expose:
- temperature
- max tokens
- additional model parameters

## Expected Outcome Model

Expected outcome means: the behavior the harness should judge as correct or incorrect for the custom test.

It can be specified through combinations of:
- behavior category
- forbidden outputs
- required outputs
- acceptable evaluation labels
- unacceptable evaluation labels

Expected outcome policy:
- optional for exploratory runs
- required to save a reusable scenario

This preserves low-friction experimentation while keeping saved scenarios rigorous.

## Evaluation Model

Exploratory runs should still be classified when possible.

Examples:
- `direct_obedience`
- `unsafe_repetition`
- `safe_summary`
- `safe_refusal`
- `safe_other`

The system should support:
- project-provided evaluators
- configured evaluator rules
- full custom evaluator logic

This is a deliberate decision. The feature is expected to be technically strong, and the evaluator layer needs to match that ambition.

That said, full custom evaluator logic should still be constrained by a safe execution model when implemented. The current design decision is product-level, not a commitment to unrestricted runtime code execution.

## Results and Drilldown

This feature should be strong on both usability and technical depth.

Result presentation should split into two layers:

### Operator Layer
- clear verdict
- evaluation label
- why the result landed there
- risk summary
- provider/model
- key response excerpt

### Technical Layer
- full response
- request metadata
- token usage
- stop reason
- tool calls
- structured evaluator outcome
- raw provider response
- raw scenario definition

This mirrors the broader UI direction already established in the operator console.

## Save, Export, and Reuse

The first version should support:
- saving scenario definitions
- optionally saving run artifacts
- manual export/import of scenario files

This gives:
- reuse
- reproducibility
- portability

It also leaves room for a later built-in shared library.

## Relationship to Canonical Benchmarks

Custom scenarios should remain separate from canonical benchmarks.

Reason:
- canonical benchmark suites are expected to be hardened and project-controlled over time
- custom scenarios are user-authored and should not weaken the meaning of official benchmark reporting

This separation should remain explicit in both product language and data model.

## Data and Artifact Model

The system will likely need two distinct artifact types:

### Scenario Definition
- reusable
- editable
- exportable
- importable

### Scenario Run Artifact
- immutable result of one execution
- includes response, metadata, evaluator output, and references to the scenario definition used

This is consistent with the distinction already established between current run state and selected saved artifacts elsewhere in the console.

## Primary UX Risks

### 1. Too much free-form text
This would make the feature flexible but weak, messy, and hard to compare.

### 2. Too much rigidity
This would make the feature look serious but feel unusable in real investigations.

### 3. Weak trust-boundary labeling
This would undermine the core security framing of the product.

### 4. No clear operator summary
This would make the feature too technical for non-specialist users.

### 5. No real technical drilldown
This would make the feature too shallow for researchers.

## Recommended Product Framing

The feature should be described as:

**Custom Test**

Supporting language:
- design a scenario
- define trusted and untrusted inputs
- run the attack
- inspect the result
- save the scenario
- export the scenario

Avoid framing it as:
- “free-form prompt playground”
- “manual try anything mode”

That language would undersell the rigor the product is trying to establish.

## Open Design Questions for the Next Stage

These should be resolved in the next design document before implementation:

1. What safe mechanism will support “full custom evaluator logic”?
2. What should the scenario file format be?
3. How much of the advanced editor is form-driven versus structured text editing?
4. How should multi-provider execution be represented in one run artifact?
5. How should tool policies be expressed in guided mode?
6. How much validation should be enforced before an exploratory run can execute?
7. Should custom scenarios support templated variables for repeated attack variants?

## Recommended Next Document

The next document should translate this product design into:
- scenario schema
- UI information architecture
- evaluator architecture
- storage model
- execution flow
- non-goals and safeguards for implementation
