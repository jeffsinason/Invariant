# Invariant Front-End Architecture

## Purpose

This document outlines the design considerations, technology choices, and implementation direction for a live front-end that can be used to run prompt injection attempts against the Invariant harness.

Invariant is an EchoForgeX project. The front-end should support the research goal of building an industry-standard framework for prompt injection validation and broader AI security.

The front-end is not a separate system. It should act as an operator layer on top of the existing harness, benchmark tooling, and saved artifact model.

## Related Documents

This document describes the front-end architecture baseline.

Related documents:
- [phased_build_plan.md](phased_build_plan.md)
- [ui_roadmap.md](ui_roadmap.md)
- [custom_injection_testing_user_manual.md](custom_injection_testing_user_manual.md)
- [custom_injection_testing_design.md](custom_injection_testing_design.md)
- [custom_injection_testing_technical_design.md](custom_injection_testing_technical_design.md)
- [custom_injection_testing_help_ui_spec.md](custom_injection_testing_help_ui_spec.md)

## Goals

The front-end should allow a user to:
- run a single case against a selected provider and model
- run a benchmark matrix across multiple cases
- compare provider behavior side by side
- inspect saved run artifacts and benchmark reports
- submit custom attack prompts for exploratory testing

The front-end should also reinforce research rigor by preserving traceability, comparability, and repeatability.

## Core Design Principles

### 1. Harness-First Execution

The existing Python harness remains the execution engine.

The UI should invoke:
- case execution through the current runner layer
- benchmark execution through the batch and benchmark layer
- result persistence through the existing result store

This keeps one source of truth for:
- case definitions
- vulnerability evaluation
- provider integrations
- saved artifact structure

### 2. Server-Side Provider Access

Provider keys must remain on the server side.

The browser should never directly call:
- OpenAI
- Anthropic

Instead, the front-end should call a backend API that wraps the harness.

### 3. Research-Grade Traceability

Each run should be recorded as an auditable experiment.

The front-end should make it easy to inspect:
- provider
- model
- case name
- request metadata
- usage
- tool calls
- raw response
- normalized verdict
- timestamp
- saved artifact path
- structured errors when runs fail

### 4. Comparison as a First-Class Workflow

The interface should support direct provider comparison because comparative security behavior is one of the primary research values of the system.

### 5. Safe Handling of Unsafe Content

The UI will intentionally accept and display adversarial prompts and model responses.

That means:
- no rendering of raw HTML from model output
- all untrusted text rendered as plain text
- clear separation between user input, retrieved content, system context, and model output

## Recommended Technology Stack

### Front-End

**React + TypeScript + Vite**

Why:
- fast iteration for an operator console
- strong typing for evolving API schemas
- simple local development model
- easy path to production build artifacts

Reference:
- [Vite Getting Started](https://vite.dev/guide/)

### Back-End

**FastAPI**

Why:
- the harness already lives in Python
- easy typed API layer
- lightweight enough for a research platform
- good fit for async provider-backed execution if needed later

Reference:
- [FastAPI](https://fastapi.tiangolo.com/)

### Persistence

**SQLite**

Why:
- simple local-first research workflow
- easy to inspect
- enough for run history, benchmark history, and metadata indexing
- JSON support is built in for structured fields

References:
- [SQLite Documentation](https://sqlite.org/docs.html)
- [SQLite JSON Functions](https://www.sqlite.org/json1.html)

### End-to-End UI Testing

**Playwright**

Why:
- reliable end-to-end browser testing
- good fit for operator workflows
- strong debugging and trace tooling

References:
- [Playwright Running Tests](https://playwright.dev/docs/running-tests)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

## Proposed System Architecture

### Front-End Application

The current console is organized into three tabs:
- `Run Case`
- `Run Benchmark`
- `Artifacts`

This reflects three distinct workflows:
- execute a single case and inspect the live result
- execute a benchmark and compare it to a saved benchmark
- compare saved artifacts and provider-level benchmark behavior

### Back-End API Layer

The front-end should call a backend API that exposes a thin wrapper around the harness.

Suggested endpoints:
- `GET /cases`
- `GET /providers`
- `POST /runs/case`
- `POST /runs/benchmark`
- `GET /runs`
- `GET /runs/{id}`
- `GET /benchmarks`
- `GET /benchmarks/{id}`

### Execution Layer

The API layer should use existing harness components wherever possible:
- `SimpleRunner`
- `BatchRunner`
- benchmark normalization and report builders
- result store helpers

### Storage Layer

Store indexed run and benchmark metadata in SQLite.

Possible tables:
- `runs`
- `benchmarks`
- `benchmark_runs`
- `custom_prompts`

Raw JSON artifacts can continue to live in `harness/results`, with SQLite storing references and summary metadata.

## Front-End Feature Set

### 1. Run Case Tab

The `Run Case` tab is optimized for single-case execution and immediate analysis.

Current controls:
- provider selector
- model selector
- case selector
- optional custom model override
- save-artifact toggle
- run button

Current outputs:
- `Current Run Case` for the most recent case execution in the current session
- `Selected Case Result` for any saved run artifact
- operator-first result summary
- response text
- evaluation label when present
- expandable technical metadata and raw response payload

### 2. Run Benchmark Tab

The `Run Benchmark` tab is optimized for benchmark execution and benchmark-to-benchmark comparison.

Current layout:
- compact benchmark run control at the top
- side-by-side benchmark columns below

Current benchmark controls:
- provider selector
- model selector
- case multi-select
- run button

Current comparison model:
- `Current Benchmark Controls`
  - family filter
  - sort order
- `Selected Benchmark Controls`
  - saved benchmark selector
  - family filter
  - sort order
- `Current Benchmark`
  - most recent benchmark from the current session
- `Selected Benchmark`
  - independently selected saved benchmark artifact

Current outputs:
- summary counts
- grouped family breakdown
- normalized per-case results
- saved benchmark artifact reference
- clearer distinction between current-session state and selected historical artifact

### 3. Artifacts Tab

The `Artifacts` tab is reserved for cross-artifact analysis rather than live execution.

Current sections:
- `Run Comparison`
- `Benchmark Comparison`
- `Provider Differences`

Comparison dimensions currently supported:
- vulnerable vs safe
- evaluation label differences
- response-pattern differences
- benchmark-level differences across providers
- usage, stop reason, and tool-call divergence when available

### 4. History and Artifact Inspection

The console is built around saved artifacts, not only fresh executions.

The current design uses selectors and comparison panels instead of long artifact lists on the main execution tabs. This makes the workflow clearer:
- current-session result stays separate from saved historical artifact
- saved benchmark selection stays separate from current benchmark execution
- artifact comparison lives in the artifacts workflow instead of being mixed into run controls

## Security Considerations

### Provider Key Safety

- keep keys in backend environment configuration only
- never expose keys in browser bundles

### Output Rendering Safety

- render response bodies as plain text
- never trust provider output as markup

### Rate Limiting and Cost Control

The API layer should eventually support:
- per-user or per-session rate limits
- benchmark case count limits
- provider request budgeting

### Artifact Integrity

Saved runs should remain immutable once written so benchmark outputs can be cited and compared later.

## UX Considerations

The first version should feel like an operator console, not a marketing site.

That means:
- fast path to run an attack
- fast path to compare providers
- minimal decorative UI
- clear presentation of verdicts and evidence

The interface should privilege:
- speed
- clarity
- repeatability

## Suggested Build Order

### Phase 1 — API Wrapper

Build a FastAPI layer that exposes:
- case execution
- benchmark execution
- run listing
- benchmark listing

### Phase 2 — Operator Console

Build a Vite + React + TypeScript UI with:
- tabbed case, benchmark, and artifact workflows
- operator-first summaries
- technical drilldowns
- side-by-side benchmark comparison

### Phase 3 — Comparative Research Workflow

Add and refine:
- richer run comparison
- richer benchmark comparison
- clearer provider-difference views
- family-level filters and risk-oriented sorting

### Phase 4 — UI Test Coverage

Add Playwright coverage for:
- case execution flow
- benchmark execution flow
- run-history rendering
- provider comparison rendering

For the post-baseline evolution of the console and custom-test workflows, see [ui_roadmap.md](ui_roadmap.md).

## Relationship to the Next Framework Phase

The front-end is not the final framework.

Its role is to accelerate:
- empirical testing
- case iteration
- provider comparison
- operator feedback
- evidence review by both technical and non-technical users

That directly informs the next major phase: building the actual defensive framework for preventing prompt injection through trust boundaries and system-level controls.

## Recommendation

Use:
- React + TypeScript + Vite for the front-end
- FastAPI for the backend API wrapper
- SQLite for metadata persistence
- Playwright for front-end end-to-end testing

This is the most coherent path because it preserves the Python harness as the execution core while giving the project a practical, research-friendly operator interface.
