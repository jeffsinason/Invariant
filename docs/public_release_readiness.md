# Invariant Public Release Readiness

## Purpose

This document defines what Invariant should be considered ready to deliver as a
public open source software release.

It has two jobs:
- define the deliverable clearly
- provide a release-readiness checklist against that definition

This is not a product vision document.

It is a practical release document for deciding whether Invariant is ready to
be distributed publicly as an EchoForgeX-backed open source offering.

## Release Position

Invariant should be released publicly first as:

- an **open source technical preview / alpha**
- positioned as an **EchoForgeX project**
- framed as the **testing and operator-facing research surface** for the larger
  injection prevention framework

It should not be presented yet as:
- a polished end-user consumer product
- a managed SaaS platform
- a finished injection prevention framework

The public offer should be honest about what it is:

**Invariant is an open source harness and operator console for prompt injection
and trust-boundary security testing in AI systems.**

It also acts as:
- a public proof point for EchoForgeX
- a practical on-ramp to the broader injection prevention framework
- a way to demonstrate the system-level security thesis in working software

## Deliverable Definition

The public deliverable is ready when an outside technical user can:

1. understand what Invariant is
2. install and start it without private tribal knowledge
3. run canonical cases against at least one provider
4. run benchmarks and inspect artifacts in the UI
5. author and run a custom injection test
6. interpret the result correctly using the included documentation
7. understand the boundaries of the current release
8. understand how this project connects to EchoForgeX and the future framework

## What Must Be Delivered

The release must include all of the following.

### 1. Open source repository

- public GitHub repository
- clean default branch
- no obviously internal-only files or secrets
- project description and positioning in the repository landing area

### 2. License and contribution posture

- explicit OSS license
- contribution guidance
- issue reporting path
- security disclosure path

Without these, public OSS distribution is incomplete.

### 3. Working local install path

An outside user must be able to:
- clone the repository
- install the required dependencies
- start the backend
- start the frontend
- understand how to configure provider keys

This should not require reading internal design documents to get started.

### 4. Canonical benchmark suite

The release must include:
- documented canonical cases
- benchmark execution
- saved benchmark artifacts
- result interpretation guidance

### 5. Custom injection testing

The release must include:
- guided custom testing
- advanced custom testing
- scenario save/load behavior
- run artifact and run-group inspection
- documentation strong enough to make the feature usable

This is one of the main differentiators of the package and should be treated as
part of the deliverable, not an experimental footnote.

### 6. Operator console

The UI should support:
- `Run Case`
- `Run Benchmark`
- `Custom Test`
- `Artifacts`

And the workflows should be understandable without reading source code.

### 7. Documentation set

The public release needs a documentation set that covers:
- what the project is
- how to run it
- how to use the UI
- how to use custom injection testing
- how to interpret results
- what is not yet part of the release

### 8. EchoForgeX framing

The project should visibly communicate:
- that Invariant is an EchoForgeX project
- that the harness is part of a broader injection prevention and AI security
  architecture
- that the OSS offering is intended to support the larger framework direction

## Required Release Hardening Workstreams

Before the first public OSS release, the following four workstreams should be
treated as required build tracks, not optional cleanup.

### 1. OSS licensing build

The release must include:
- a chosen OSS license
- a committed `LICENSE` file
- confirmation that the selected license matches the intended EchoForgeX
  distribution strategy

This is a release blocker. The project should not be distributed publicly as
open source without an explicit license.

### 2. Contributing guidance build

The release must include:
- a `CONTRIBUTING.md`
- clear guidance for issues, pull requests, and contribution expectations
- a clear statement of what kinds of contributions are in and out of scope

This is necessary because public OSS distribution invites outside contribution,
and the project should define that relationship clearly.

### 3. Security disclosure path build

The release must include:
- a documented vulnerability disclosure path
- a clear location for reporting security issues
- guidance on whether to use public issues or a private disclosure channel

This matters especially because Invariant is explicitly a security-related
project. Public release without a security reporting path would be weak.

### 4. Quickstart hardening build

The release must include:
- one clean outsider quickstart path
- explicit prerequisites
- backend and frontend startup steps
- provider-key setup guidance
- validation that the quickstart works in a clean environment

This is not only a docs task. It is a product hardening task. If the quickstart
is fragile or ambiguous, the public release is not ready.

## What Does Not Need To Be Finished For First Public Release

The first public release does **not** require:
- the full injection prevention framework implementation
- hosted SaaS deployment
- enterprise auth and multi-user administration
- assistant-led custom scenario creation
- full packaging as a desktop product
- every future UI refinement from the roadmap

These should remain explicitly out of scope for the first OSS public release.

## Readiness Standard

The project is ready for public release when it reaches this standard:

### Installable

A technically capable outsider can get it running in reasonable time.

### Understandable

A technically capable outsider can tell:
- what the product does
- what the major workflows are
- what problem it solves

### Demonstrable

A technically capable outsider can produce a meaningful artifact with it.

### Honest

The release clearly communicates what is alpha, what is stable enough for
testing, and what is still future-facing.

### Defensible

The repo, docs, and product framing make a coherent technical argument for why
the tool exists and how it relates to injection prevention.

## Public Release Checklist

Use this checklist before opening the project for broad public use.

### A. Repository and OSS basics

- [ ] confirm repository visibility and owner strategy
- [ ] add an explicit OSS license
- [ ] commit a `LICENSE` file
- [ ] confirm the chosen license matches EchoForgeX distribution intent
- [ ] add a `CONTRIBUTING.md`
- [ ] define contribution scope and expectations clearly
- [ ] add issue templates
- [ ] add a security reporting / vulnerability disclosure path
- [ ] add a dedicated security reporting document if needed
- [ ] confirm no secrets, private tokens, or internal-only data remain in repo
- [ ] confirm `.gitignore` is sufficient

### B. Positioning and messaging

- [ ] tighten the top-level README for public readers
- [ ] clearly state Invariant is an EchoForgeX project
- [ ] clearly state what the release is:
  - OSS harness
  - operator console
  - injection testing platform
- [ ] clearly state what the release is not:
  - finished prevention framework
  - hosted service
  - enterprise platform
- [ ] add screenshots or short UI captures
- [ ] add a concise “why this matters” section tied to trust boundaries and
  system-level controls

Current captured UI assets for public packaging:
- [invariant-console-run-case.png](assets/invariant-console-run-case.png)
- [invariant-console-run-benchmark.png](assets/invariant-console-run-benchmark.png)
- [invariant-console-custom-test.png](assets/invariant-console-custom-test.png)
- [invariant-console-artifacts.png](assets/invariant-console-artifacts.png)

### C. Installation and setup

- [ ] document environment prerequisites
- [ ] document backend install
- [ ] document frontend install
- [ ] document provider key configuration
- [ ] provide one clean quickstart path from clone to running UI
- [ ] verify the quickstart can be followed without reading internal design docs
- [ ] verify quickstart on a clean machine/worktree
- [ ] verify failure messages are understandable when keys are missing

### D. Product workflows

- [ ] verify `Run Case` workflow end to end
- [ ] verify `Run Benchmark` workflow end to end
- [ ] verify `Custom Test` workflow end to end
- [ ] verify `Artifacts` workflow end to end
- [ ] verify saved scenario / run / run-group flows
- [ ] verify provider comparison remains understandable

### E. Canonical testing surface

- [ ] verify canonical case registry is documented
- [ ] verify benchmark family coverage is documented
- [ ] verify provider support is documented
- [ ] verify expected evaluator labels are documented
- [ ] verify result interpretation is documented
- [ ] verify live-provider paths are clearly marked as dependent on API keys

### F. Custom injection testing

- [ ] verify the user manual is sufficient for a first-time user
- [ ] verify guided mode can be used without internal help
- [ ] verify advanced mode is understandable to a technical user
- [ ] verify import/export works as documented
- [ ] verify evaluator configuration is documented well enough to avoid misuse
- [ ] verify templates, help text, placeholders, and examples are coherent

### G. Technical quality

- [ ] run backend automated tests
- [ ] run frontend automated tests
- [ ] run frontend build
- [ ] verify mock provider flow
- [ ] verify at least one live-provider path in released docs
- [ ] verify no obviously broken UI state remains
- [ ] verify raw errors are not leaking confusing implementation details in
  common flows

### H. Release hygiene

- [ ] create a release tag/versioning approach
- [ ] define alpha/preview naming
- [ ] add changelog or release notes
- [ ] define known limitations section
- [ ] define support expectations for OSS users
- [ ] define how future roadmap items are tracked publicly

Current release-hygiene assets:
- [CHANGELOG.md](../CHANGELOG.md)
- [support_and_limitations.md](support_and_limitations.md)

### I. EchoForgeX linkage

- [ ] make the EchoForgeX relationship explicit in README and docs
- [ ] explain how this OSS release relates to the future injection prevention
  framework
- [ ] make clear that Invariant is both useful standalone and strategically part
  of a larger architecture

## Release Decision Tiers

Use these tiers to decide how publicly to distribute the project.

### Tier 1 — Private Review

Ready when:
- core workflows work
- docs exist but are incomplete
- install path may still be rough

Channels:
- direct sharing
- private demos
- design partner review

### Tier 2 — Public Technical Preview

Ready when:
- the checklist above is mostly complete
- install path is documented and usable
- docs are coherent
- the project is honest about its alpha state

Channels:
- public GitHub repository
- EchoForgeX page pointing to GitHub
- selective public posts and outreach

### Tier 3 — Broad Public OSS Release

Ready when:
- installation is cleaner
- documentation is stronger
- release hygiene is in place
- issue handling and contribution paths are clear
- the project can absorb public attention without confusion

Channels:
- public GitHub
- EchoForgeX site
- broader community announcement

## Recommended First Public Channel

The best first public channel is:

- **GitHub as a public technical preview**

Supported by:
- an EchoForgeX page describing the project and linking to the repository

This is the right first channel because Invariant is currently:
- technical
- open source
- research and operator focused
- most useful to developers and security-minded practitioners first

## Current Likely Status

Based on the current project shape, the most realistic classification is:

- suitable for private/internal use
- suitable for invite-only alpha
- close to public technical preview
- not yet ideal for broad general public OSS launch without additional release
  hygiene

The most likely blockers for broad public release are:
- license and OSS scaffolding
- installation hardening and quickstart polish
- public-facing packaging and screenshots
- security/disclosure and contribution guidance

## Recommended Next Actions

1. close the OSS scaffolding gaps:
   - license
   - contributing
   - disclosure policy
2. build the release hardening workstreams explicitly:
   - OSS licensing
   - contributing guidance
   - security disclosure path
   - quickstart hardening
3. tighten README and quickstart for outsiders
4. verify first-run experience on a clean environment
5. capture UI screenshots/GIFs for public presentation
6. package the first release as a public technical preview

## Related Documents

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [SECURITY.md](../SECURITY.md)
- [current_release_hardening_pass.md](current_release_hardening_pass.md)
- [provider_expansion_feasibility.md](provider_expansion_feasibility.md)
- [frontend_architecture.md](frontend_architecture.md)
- [phased_build_plan.md](phased_build_plan.md)
- [ui_roadmap.md](ui_roadmap.md)
- [custom_injection_testing_user_manual.md](custom_injection_testing_user_manual.md)
