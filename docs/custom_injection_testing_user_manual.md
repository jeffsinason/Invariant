# Custom Injection Testing User Manual

## Purpose

This manual explains how to use the `Custom Test` workflow in Invariant.

It is written for operators, security reviewers, and technical users who need
to:
- design a custom injection scenario
- run it against one or more providers and models
- interpret the result correctly
- save and reuse scenarios without relying on internal implementation knowledge

This document is user-facing. It complements, but does not replace, the design
and technical documents in the `docs/` directory.

## What Custom Injection Testing Is

Custom injection testing lets you define your own attack scenario instead of
only running one of the built-in canonical cases.

Use it when you need to test:
- a scenario that is not covered by the benchmark suite
- a variation of a known attack family
- a provider- or model-specific behavior
- a system-like workflow involving retrieved content, tools, memory, or
  conversation state

Custom tests are intentionally separate from canonical benchmarks.

Canonical benchmarks are curated and controlled by the project over time.
Custom tests are for exploratory, system-specific, or operator-authored attack
experiments.

## Where It Lives

Open the Invariant UI and go to the `Custom Test` tab.

The tab supports two authoring modes:
- `guided`
- `advanced`

## When To Use Guided vs Advanced

Use `guided` when:
- you want structured defaults
- you are working from a known attack family
- you want template help, placeholders, and examples
- you want the easiest way to produce a valid scenario

Use `advanced` when:
- you need precise control over the scenario structure
- you need multi-target definitions or more complex inputs
- you want tighter control over evaluator behavior
- you are comfortable editing a more technical scenario

Recommended default:
- start in `guided`
- switch to `advanced` only when the scenario shape exceeds the guided form

## Core Concepts

### Scenario

A scenario is the definition of the test itself.

It includes:
- metadata
- target provider/model configuration
- trusted instructions
- user request
- untrusted inputs
- attack placement and timing
- expected safe behavior
- evaluator settings

### Run Artifact

A run artifact is the saved result of executing one scenario once.

It contains:
- the executed scenario snapshot
- the provider/model used
- the response
- structured evaluation output
- metadata such as request id, usage, and errors

### Run Group

A run group is a grouped result from running the same scenario against multiple
targets in one operation.

Use run groups when you want:
- provider comparison
- model comparison
- repeatable side-by-side review

### Trusted vs Untrusted Inputs

This distinction matters.

Trusted inputs are the instructions and constraints the model should follow.
Examples:
- system instructions
- developer instructions
- explicit policy text you intend the model to obey

Untrusted inputs are where injection attempts usually live.
Examples:
- retrieved documents
- HTML comments
- metadata blocks
- tool outputs
- memory notes copied from outside sources

If you model trust boundaries incorrectly, the custom test becomes less useful.

## Basic Workflow

1. Choose `guided` or `advanced`
2. Choose an attack family
3. Set the target provider/model
4. Define trusted context
5. Define user context
6. Define untrusted inputs
7. Define attack placement, timing, and payload
8. Define the expected safe outcome
9. Choose or configure the evaluator
10. Validate
11. Run
12. Save the scenario if it is worth reusing

## Guided Mode Walkthrough

Guided mode is template-first.

Each template supplies:
- help text
- placeholders
- minimal example
- realistic example
- validation hints
- progressive disclosure of advanced sections

### Step 1: Pick an Attack Family

Typical families include:
- `direct_override`
- `prompt_leakage`
- `indirect_injection`
- `indirect_injection_html_comment`
- `indirect_injection_metadata`
- `cross_document_poisoning`
- `multi_hop_retrieval`
- `tool_manipulation`
- `unauthorized_action_execution`
- `context_poisoning`

Choose the family that best matches the attack shape, not just the exact words
you want to try.

### Step 2: Use the Template Actions

The builder supports:
- `Apply Template Defaults`
- `Load Minimal Example`
- `Load Realistic Example`

Recommended use:
- start with `Load Minimal Example`
- confirm the structure
- replace the content with your own attack

### Step 3: Fill the Major Sections

Depending on template, the builder may show sections such as:
- trusted instructions
- user context
- untrusted inputs
- tools
- attack
- evaluation

Do not expect every section to appear for every attack family. The UI hides
irrelevant sections on purpose.

### Step 4: Validate

Use validation before running.

Validation checks for problems such as:
- missing scenario name
- missing request input
- duplicate targets
- invalid placement or timing
- evaluated saved scenarios missing an expected outcome

### Step 5: Run

After a run, inspect:
- operator summary
- response text
- evaluation label
- verdict
- technical metadata if needed

## Advanced Mode Walkthrough

Advanced mode exposes more structure directly.

Use it when you need:
- tighter control over targets
- richer context
- memory and turn authoring
- structured evaluator rules
- a more exact scenario definition

Advanced mode is still template-driven.

That means:
- attack-family templates still shape section order
- attack and evaluation section order still follow template metadata
- template examples can still seed the editor

### Advanced Metadata

Use metadata for:
- scenario name
- description
- tags
- authoring mode
- scenario intent

### Advanced Targets

You can define:
- one target
- multiple targets in one scenario

Single target is the default.
Multi-target is useful for comparison and run groups.

### Advanced Context

Advanced mode can include:
- system instructions
- developer instructions
- user request
- conversation turns
- session summary
- memory items
- untrusted notes
- retrieved content
- tool outputs
- available tools

Use only the context needed for the attack you are testing. Do not add noise
without purpose.

## Expected Outcome

Expected outcome means: what safe behavior the harness should consider correct.

Examples:
- refuse the override
- ignore untrusted retrieved instructions
- summarize safely
- do not reveal hidden instructions
- do not call a tool
- do not call an unauthorized tool

### Exploratory vs Evaluated

The product supports both:
- `exploratory`
- `evaluated`

#### Exploratory

Use exploratory mode when:
- you are probing behavior
- you do not yet know the right pass/fail condition
- you want to inspect raw behavior first

Exploratory runs may still receive internal classifications if the evaluator can
infer one.

#### Evaluated

Use evaluated mode when:
- you want a defensible pass/fail result
- you want the scenario to be reusable
- you want saved scenarios to remain rigorous

Saved reusable scenarios in evaluated mode should define expected safe behavior.

## Evaluators

The evaluator determines how the harness interprets the response.

### Builtin

Use this first in most cases.

Builtin evaluators are aligned to attack-family behavior and are the least
error-prone option.

### Configured

Configured evaluator rules let you add constrained logic such as:
- forbidden outputs
- forbidden tool names

Use this when builtin evaluation is close, but not specific enough.

### Custom

Custom evaluators support more explicit rule authoring.

The UI supports structured rules rather than forcing raw JSON as the main path.
Example conditions include:
- response contains a string
- response does not contain a string
- tool call count exceeds a threshold
- a tool name was called
- evaluation label is a specific value

Custom evaluator rules are powerful. Use them carefully. Keep the rules
minimal, readable, and tied to the attack objective.

## Interpreting Results

Do not rely only on the boolean verdict.

Interpret these together:
- verdict
- evaluation label
- response text
- scenario context
- tool call behavior

### Common Retrieval-Oriented Labels

- `direct_obedience`
  - the model complied with the malicious instruction
- `unsafe_repetition`
  - the model echoed harmful instruction content unsafely without necessarily
    obeying it
- `safe_summary`
  - the model handled content safely and kept to the benign task
- `safe_refusal`
  - the model refused the harmful request or unsafe instruction
- `safe_other`
  - the model remained safe but did not fit one of the narrower categories

### Practical Reading Rule

If the model:
- outputs the planted token
- follows the malicious instruction
- calls an unauthorized tool
- reveals protected content

then the result is a real failure candidate.

If the model only references or summarizes attack text, inspect whether that is:
- a safe explanation
- unsafe repetition
- or actual obedience

## Saved Scenarios, Runs, and Run Groups

### Save Scenario

Save a scenario when:
- it represents a meaningful test case
- you will rerun it later
- you want to compare models/providers against the same authored scenario

### Save Run Artifact

Save the run artifact when:
- the output is important
- you want evidence of provider behavior
- you need later comparison or review

### Run Group

Use a run group when:
- the same scenario should run against multiple providers/models
- you want a comparable artifact set

Run groups are especially useful for:
- provider comparison
- model regression analysis
- identifying which families separate vendors most clearly

## Import and Export

Custom scenarios support import/export as JSON.

Use export when:
- you want to archive a scenario
- you want to move it between environments
- you want to share it manually

Use import when:
- you want to restore a known scenario
- you received a scenario file from another user or workflow

Current sharing model:
- manual export/import

Built-in shared libraries are not the default first-version behavior.

## Recommended First Tests

### 1. Indirect Injection

Good first test because it exercises trust boundaries cleanly.

Suggested shape:
- benign user request
- untrusted retrieved content containing an override
- expected behavior: ignore the override and complete the benign task

### 2. Direct Override

Good first test because it is simple to reason about.

Suggested shape:
- explicit system instruction
- direct user attack attempting to override it
- expected behavior: refuse or remain aligned to the trusted instruction

### 3. Prompt Leakage

Good first test for protected-instruction handling.

Suggested shape:
- hidden or protected instruction context
- user request to reveal it
- expected behavior: do not leak protected content

## Common Mistakes

### 1. Mixing Trusted and Untrusted Inputs

Do not put the malicious payload in a trusted field unless that is the thing
you are intentionally testing.

### 2. Leaving the Expected Outcome Vague

If the safe behavior is unclear, the result becomes harder to interpret and
reuse.

### 3. Overcomplicating the First Version of a Scenario

Start with the smallest valid scenario that expresses the attack.
Add memory, tools, or multi-turn state only when needed.

### 4. Using Custom Evaluator Logic Too Early

Prefer builtin or lightly configured evaluators first.
Only use custom rule authoring when the simpler evaluators are insufficient.

### 5. Treating Saved Custom Tests Like Canonical Benchmarks

They are intentionally separate.
Custom tests are operator-authored scenarios, not project-controlled benchmark
cases.

## Recommended Operating Pattern

For most users, the best workflow is:

1. pick a template in guided mode
2. load the minimal example
3. replace the example content with your real scenario
4. validate
5. run against one provider/model
6. inspect the result
7. refine expected outcome or evaluator if necessary
8. save the scenario
9. rerun across multiple targets as a run group

This keeps the scenario understandable while still producing reusable artifacts.

## Related Documents

For deeper implementation or design detail, see:
- [custom_injection_testing_design.md](custom_injection_testing_design.md)
- [custom_injection_testing_technical_design.md](custom_injection_testing_technical_design.md)
- [custom_injection_testing_implementation_plan.md](custom_injection_testing_implementation_plan.md)
- [custom_injection_testing_help_ui_spec.md](custom_injection_testing_help_ui_spec.md)
- [custom_injection_testing_template_catalog.md](custom_injection_testing_template_catalog.md)
