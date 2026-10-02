# Current Release Hardening Pass

## Purpose

This document defines the next hardening pass for Invariant **before** public
technical preview release.

The scope here is intentionally limited:
- harden the current Invariant release as it exists now
- do not expand the release surface unnecessarily
- document additional provider candidates separately

This pass should improve release quality without diluting the current deliverable.

## Hardening Goal

Move Invariant from:
- a technically strong internal / alpha-capable project

to:
- a cleaner public technical preview that an outside technical user can
  evaluate with less friction and less ambiguity

## Hardening Principles

1. prefer clarity over new surface area
2. fix real first-run and public-repo gaps first
3. do not confuse future framework direction with current OSS deliverable
4. keep the current release centered on:
   - harness
   - operator console
   - benchmark suite
   - custom injection testing

## In Scope

### 1. OSS release hygiene

- license
- contributing guide
- security policy
- issue templates
- changelog
- known limitations and support expectations

### 2. Quickstart hardening

- outsider quickstart path
- validated setup steps
- backend install path correctness
- first-run workflow clarity

### 3. Public packaging

- README polish
- screenshots
- UI icon
- public technical preview framing

### 4. Validation and consistency

- verify core flows remain coherent
- make sure docs and actual startup steps match
- ensure the public repo reflects the actual product state

## Out of Scope For This Pass

- full prevention framework implementation
- SaaS deployment
- broad enterprise packaging
- major new workflow families
- broad refactor work unrelated to release clarity

Additional provider evaluation is relevant, but it should be treated as a
separate assessment track unless one provider is selected for immediate
pre-release inclusion.

## Current Hardening Status

### Completed in this pass so far

- OSS license added
- OSS, IP, and branding note added
- contributing guide added
- security policy added
- issue templates added
- quickstart guide added
- quickstart validated in a fresh clone
- editable install path documented for backend startup
- UI screenshots captured
- UI icon added
- changelog added
- support and limitations doc added

### Verified outcomes

- fresh-clone setup can be completed with the documented editable install path
- backend starts after `pip install -e .`
- frontend starts successfully
- mock case execution works
- mock benchmark execution works

## Remaining Hardening Items

These are the remaining items worth considering before public technical preview.

### A. README public polish

- tighten the top of the README for outside readers
- reduce architecture-heavy material above the practical value proposition
- make the first-screen repo experience more clearly product-oriented

### B. Public-preview framing

- decide exact release naming:
  - `0.1.0-alpha`
  - `technical preview`
- align README, changelog, and release notes language

### C. Dependency hygiene

- review frontend npm vulnerability output
- decide whether to remediate before preview or document as known release hygiene

### D. Final pre-release validation

- one more explicit pass through:
  - `Run Case`
  - `Run Benchmark`
  - `Custom Test`
  - `Artifacts`
- ensure screenshots still reflect the shipped UI accurately

## Recommended Decision Rule

The current release should be considered ready for public technical preview when:

1. the remaining README/public-packaging polish is complete
2. the release posture is explicitly named and consistent
3. there are no known first-run blockers
4. the current UI screenshots match the released UI
5. no governance or licensing gaps remain

## Relation To Provider Expansion

Provider expansion should be evaluated now, but not automatically bundled into
this hardening pass.

The correct sequence is:

1. finish hardening the current release
2. evaluate additional providers
3. decide whether one provider is mature enough to include immediately

This keeps the current release coherent and prevents last-minute scope creep.

## Recommended Next Actions

1. perform the final README/public-packaging polish
2. make an explicit release naming decision
3. review npm vulnerability posture
4. run one final workflow validation pass
5. separately evaluate Gemini, Grok, and a third provider candidate

## Related Documents

- [public_release_readiness.md](public_release_readiness.md)
- [quickstart.md](quickstart.md)
- [support_and_limitations.md](support_and_limitations.md)
- [frontend_architecture.md](frontend_architecture.md)
