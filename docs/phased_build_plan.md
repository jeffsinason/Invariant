# Invariant Phased Build Plan

## Purpose

This document connects the major development threads of Invariant into a single phased plan:

1. harness and benchmark suite
2. live front-end
3. injection defense framework
4. system-level AI security architecture

Invariant is an EchoForgeX project. The purpose of this phased plan is to show how the current harness work evolves into a broader AI security framework with practical defensive value.

## Guiding Principle

Invariant should evolve in a way that preserves continuity between:
- research
- testing
- operator workflows
- defensive controls

The benchmark suite should not be abandoned when the front-end appears.
The front-end should not be abandoned when the defensive framework begins.
Each phase should build on the previous one.

## Phase 1 — Harness and Benchmark Suite

### Objective

Create a credible, extensible prompt injection test harness and benchmark foundation.

### What This Phase Produces

- provider adapters
- canonical security test cases
- normalized results
- batch execution
- benchmark comparison artifacts
- automated tests

### Current Status

This phase is already substantially in place.

Current capabilities include:
- OpenAI and Anthropic provider testing
- benchmark matrix execution
- multiple attack classes
- structured result saving
- mock-backed testing
- live-provider validation paths

### Remaining Work in Phase 1

- continue refining evaluator quality from live findings
- add more provider coverage if needed
- improve benchmark comparability and reporting polish
- keep expanding case depth carefully

### Why Phase 1 Matters

Without this phase, the later framework would lack:
- evidence
- repeatability
- baseline measurements
- credibility

This phase establishes the empirical backbone of the project.

## Phase 2 — Live Front-End

### Objective

Provide an operator-facing interface for running attack attempts, inspecting results, and comparing provider behavior.

### What This Phase Produces

- a backend API wrapper around the harness
- a front-end for case execution and benchmark execution
- run history
- benchmark history
- provider comparison views
- artifact inspection

### Relationship to Phase 1

The front-end should use the harness as its execution layer.

It should not duplicate:
- case logic
- benchmark logic
- provider adapters
- result normalization

### Why Phase 2 Matters

This phase turns the harness from a developer-only tool into an operational research interface.

It supports:
- rapid experimentation
- live investigations
- side-by-side provider comparison
- easier collaboration across technical and research workflows

### Design Direction

Recommended stack:
- React + TypeScript + Vite
- FastAPI
- SQLite
- Playwright

This phase is the bridge between research code and a usable research platform.

Supporting front-end planning documents for this phase:
- [frontend_architecture.md](/Users/jeffreysinason/Development/Invariant/docs/frontend_architecture.md)
- [ui_roadmap.md](/Users/jeffreysinason/Development/Invariant/docs/ui_roadmap.md)

## Phase 3 — Injection Defense Framework

### Objective

Move from measuring prompt injection risk to actively helping systems resist prompt injection.

### What This Phase Produces

- trust-aware context construction
- policy-aware execution controls
- retrieval sanitization
- tool authorization boundaries
- output validation layers
- deterministic control surfaces for AI systems

### Relationship to Phase 1 and Phase 2

Phase 1 tells the team what failures matter.
Phase 2 makes those failures observable and easier to explore.
Phase 3 introduces mechanisms that can reduce or prevent those failures.

### Core Idea

The framework should not attempt to solve prompt injection purely with better prompts.

Instead, it should enforce:
- trust boundaries
- least privilege
- system-level controls
- validation before action

### Why Phase 3 Matters

This is the point where Invariant becomes more than a benchmark.

It becomes a practical framework for improving AI system security.

## Phase 4 — System-Level AI Security Architecture

### Objective

Extend Invariant beyond single-model evaluation and isolated controls into a full architecture for securing AI applications composed of multiple interacting components.

### What This Phase Produces

- security architecture for multi-component AI systems
- explicit trust zones
- control-plane enforcement layers
- support for composed AI systems
- support for multiple model roles
- durable observability and governance patterns

### What “System-Level” Means Here

System-level architecture includes:
- models under test
- AI components inside the protected application
- optional AI components in the control plane
- deterministic enforcement layers
- policy and validation checkpoints

### Why Phase 4 Matters

Prompt injection is not only a model behavior problem.

It is a systems problem.

This phase is where Invariant fully aligns with the whitepaper thesis:
- prompt injection is a trust-boundary failure
- resilient systems require system-level controls

## Cross-Phase Dependency Model

Each phase supports the next:

### Phase 1 -> Phase 2

The front-end becomes useful because the harness already exists.

### Phase 2 -> Phase 3

The operator interface reveals:
- which attacks recur
- which providers fail where
- which controls are worth building first

### Phase 3 -> Phase 4

The defensive framework becomes the foundation for broader AI security architecture rather than remaining a collection of case-specific mitigations.

## Recommended Build Order

### Immediate Focus

Continue closing remaining quality and usability gaps in the harness and benchmark suite while beginning front-end implementation planning.

### Near-Term Build Sequence

1. stabilize and polish benchmark execution
2. build the API layer
3. build the minimal operator front-end
4. expand live comparison workflows

### Mid-Term Build Sequence

1. define defensive framework interfaces
2. build trust-aware context and execution controls
3. connect defensive controls to the front-end and benchmark workflows

### Long-Term Build Sequence

1. add support for composed AI systems
2. add support for control-plane AI components
3. formalize the full security architecture

## Decision Rule for Future Work

When choosing new work, ask:

Does this improve one of the following?
- empirical rigor
- operator usability
- defensive capability
- architectural clarity

If yes, it likely belongs in the phased plan.

If not, it may be premature.

## Summary

Invariant should develop through four connected phases:

1. **Harness and Benchmark Suite**  
   Establish the testing and measurement backbone.

2. **Live Front-End**  
   Turn the harness into a practical operator-facing research platform.

3. **Injection Defense Framework**  
   Build mechanisms that actively reduce prompt injection risk.

4. **System-Level AI Security Architecture**  
   Extend the framework into a full architecture for securing composed AI systems.

This sequence keeps the project coherent, research-grounded, and directly aligned with EchoForgeX's long-term objective.
