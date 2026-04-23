# Invariant UI Roadmap

## Purpose

This document captures the planned UI evolution for future Invariant releases.

The goal is not just to add more screens. The goal is to make the harness:
- easier to operate
- easier to understand
- better at surfacing meaningful security findings
- deeper in technical drilldown when expert users need it

This roadmap assumes the current baseline UI already exists:
- `Run Case`
- `Run Benchmark`
- `Custom Test`
- `Artifacts`

## Roadmap Principles

All future UI changes should support at least one of these:
- clearer operator workflow
- clearer benchmark interpretation
- stronger custom-test usability
- stronger artifact comparison
- better separation between operator summary and technical detail
- better trust-boundary visibility

UI changes should avoid:
- adding panels without a clear workflow owner
- mixing “current” and “selected” state ambiguously
- forcing users to read raw JSON first
- burying comparison controls away from the thing being compared

## Release Structure

The roadmap is organized by likely release waves, not exact dates.

---

## Release A: Usability Hardening

### Goal

Make the current console easier to use day to day without changing the underlying platform model.

### Planned UI Work

#### 1. Benchmark Family Navigation
- add family chips or segmented filters above benchmark results
- allow one-click switching between:
  - Core Prompt Security
  - Retrieval / Indirect Injection
  - Tools / Action Abuse
  - Session / Memory
- keep current family filter dropdown as fallback if needed

#### 2. Top Risks Strip
- add a compact benchmark summary strip for:
  - direct obedience count
  - unsafe repetition count
  - error count
  - most risky case family
- show this for:
  - current benchmark
  - selected benchmark

#### 3. Clearer Provider Difference Presentation
- strengthen the provider-difference dashboard in `Artifacts`
- show:
  - strongest provider by family
  - weakest provider by family
  - delta in direct obedience counts
  - delta in unsafe repetition counts

#### 4. Drill-Through Navigation
- from a benchmark result row, open the matching run artifact directly
- from a custom run group row, open the matching individual run
- from a scenario comparison row, open the scenario definition

### Outcome

This release should make the current UI materially easier to read and navigate, especially during repeated benchmark work.

---

## Release B: Custom Test UX Maturity

### Goal

Make `Custom Test` one of the strongest user-facing capabilities in the product.

### Planned UI Work

#### 1. Template-Driven Help System
- render template intro, help, placeholders, and examples more prominently
- add:
  - “What this tests”
  - “What failure looks like”
  - “Safe behavior”
  - “Common setup mistakes”

#### 2. Better Guided Builder Structure
- make the guided builder feel more like a task wizard without becoming a separate system
- likely stages:
  - target
  - trusted context
  - untrusted context
  - attack payload
  - expected safe outcome
  - evaluator

#### 3. Better Matrix Targeting UX
- replace simple text and repeated controls with clearer target rows
- allow:
  - add target
  - remove target
  - duplicate target with different model
  - run same scenario across multiple providers/models cleanly

#### 4. Better Scenario Save / Import / Export UX
- make saved scenario handling more explicit
- support:
  - save as new scenario
  - update saved scenario
  - export scenario file
  - import scenario file

#### 5. Better Run Group UX
- for multi-target custom runs, show:
  - run-group summary
  - per-target result tiles
  - side-by-side result comparison
  - response class distribution

### Outcome

This release should make custom testing feel deliberate and usable instead of merely powerful.

---

## Release C: Advanced Editor Maturity

### Goal

Turn the advanced editor from “structured technical form plus JSON fallback” into a first-class expert workflow.

### Planned UI Work

#### 1. Full Subsection Renderer
- remove remaining ad hoc subsection rendering
- let the catalog declare:
  - subsection order
  - subsection titles
  - subsection summaries
  - field membership

#### 2. Template-Specific Advanced Layout
- allow advanced templates to differ more significantly by attack family
- examples:
  - tool scenarios emphasize tools and authorization
  - retrieval scenarios emphasize document context
  - context poisoning scenarios emphasize turns and memory

#### 3. Evaluator Rule Authoring Improvements
- improve custom evaluator rule authoring with:
  - clearer condition rows
  - visual grouping of “when” and “then”
  - rule validation feedback
  - easier fallback policy editing

#### 4. Technical Preview Pane
- add a live schema preview that reflects the current structured editor state
- keep raw JSON visible as an inspection layer, not the only expert view

### Outcome

This release should make advanced-mode authoring a strong expert workflow without reverting to raw JSON dependence.

---

## Release D: Artifact Intelligence and Comparison

### Goal

Make the `Artifacts` tab the main analysis surface for serious evaluation work.

### Planned UI Work

#### 1. Benchmark-to-Benchmark Comparison
- compare two saved benchmarks directly
- show:
  - case deltas
  - family deltas
  - provider/model deltas
  - classification shifts

#### 2. Scenario-to-Result Traceability
- from a saved custom scenario, show:
  - all runs derived from it
  - all run groups derived from it
  - provider distribution
  - historical result drift

#### 3. Classification Analytics
- surface counts by:
  - `direct_obedience`
  - `unsafe_repetition`
  - `safe_summary`
  - `safe_refusal`
  - `safe_other`
  - `error`

#### 4. Time-Oriented Artifact Views
- filter and sort saved artifacts by:
  - provider
  - model
  - family
  - time range
  - vulnerability class

### Outcome

This release should make the UI much more useful as a security analysis surface, not only an execution surface.

---

## Release E: Assistant-Led Custom Testing

### Goal

Add a more approachable front door for custom testing without replacing the structured model.

### Planned UI Work

#### 1. Assistant-Led Scenario Drafting
- user describes what they want to test in plain language
- assistant maps that into:
  - attack family
  - trust-boundary setup
  - attack payload
  - expected outcome
  - evaluator choice

#### 2. Review Before Run
- generated scenario must always be shown in structured form before execution
- user can edit guided or advanced fields before running

#### 3. Assistant Suggestions
- suggest:
  - stronger attack variants
  - missing trust-boundary context
  - expected outcome defaults
  - evaluator defaults

### Important Rule

The assistant-led layer should generate the same scenario schema already used by the builder.

It must not become a separate authoring system.

### Outcome

This release should broaden accessibility without weakening rigor.

---

## Release F: Executive and Research Reporting

### Goal

Support both technical and non-technical reporting without losing evidence depth.

### Planned UI Work

#### 1. Executive Summary Views
- high-level benchmark summaries for stakeholders
- concise provider risk overviews
- family-level weakness summaries

#### 2. Research Views
- deeper classification tables
- historical drift views
- per-case comparative matrices
- downloadable structured summaries

#### 3. Presentation-Ready Export
- export benchmark summaries and comparison views in formats suitable for:
  - internal review
  - research reporting
  - investor or leadership briefings

### Outcome

This release should help Invariant communicate value clearly to multiple audiences.

---

## Cross-Cutting Improvements

These can land incrementally across releases.

### 1. Better Empty States
- every tab and panel should explain what to do next when empty

### 2. Better Error Handling
- clearer UI for:
  - provider failures
  - invalid scenarios
  - partial multi-target failures

### 3. Better State Persistence
- persist tab, filters, and selected artifacts across refresh where appropriate

### 4. Stronger Accessibility
- keyboard navigation
- focus handling
- clearer form labeling
- better contrast and status semantics

### 5. More Frontend Test Coverage
- expand coverage for:
  - benchmark comparison
  - custom run groups
  - advanced editor
  - import/export workflows
  - future assistant-led flows

---

## Recommended Implementation Order

If this roadmap is tackled pragmatically, the recommended order is:

1. Release A: Usability Hardening
2. Release B: Custom Test UX Maturity
3. Release D: Artifact Intelligence and Comparison
4. Release C: Advanced Editor Maturity
5. Release E: Assistant-Led Custom Testing
6. Release F: Executive and Research Reporting

Reason:
- the product gets immediate usability value first
- the custom test feature becomes stronger before adding more abstraction
- comparison and artifact analysis continue to improve research value
- assistant-led flows should come after the structured system is mature

---

## Definition of Success

The UI roadmap is succeeding when:
- a non-expert user can run meaningful tests without confusion
- a technical evaluator can inspect exact evidence without friction
- provider differences are obvious
- benchmark results are interpretable quickly
- custom testing feels powerful but not hostile
- the UI makes the value of the harness legible without forcing users into raw JSON or raw artifact files first
