# Support and Limitations

## Purpose

This document sets expectations for users of the public open source release of
Invariant.

It covers:
- current release limitations
- support expectations
- alpha maturity boundaries

## Release Maturity

Invariant should currently be treated as:

- an alpha / technical preview
- an open source research and operator tool
- a practical testing surface for prompt injection and trust-boundary analysis

It should not yet be treated as:
- a finished prevention framework
- an enterprise-supported platform
- a hosted managed service

## Current Limitations

### 1. Alpha workflow maturity

The product is usable, but some workflows are still evolving.

This is most visible in:
- custom injection testing complexity
- UI refinement and comparison ergonomics
- provider/model menu and discovery polish

### 2. Provider-dependent live behavior

Live provider results depend on:
- API key availability
- provider model changes
- provider-side behavior changes over time

The mock provider remains useful for deterministic local validation, but live
behavior is inherently less stable.

### 3. Canonical benchmarks are still evolving

The benchmark suite is meaningful and already differentiates providers, but:
- evaluator quality is still being refined
- some case families will continue to deepen
- benchmark coverage should still be considered under active development

### 4. Custom testing is powerful but not lightweight

Custom injection testing is one of the most important features in the project,
but it is also one of the most complex.

Users should expect:
- a meaningful learning curve
- the need to understand trust boundaries
- the need to choose evaluators carefully

### 5. Local setup is still technical

The quickstart is now documented and validated, but the product is still aimed
at technical users.

Users should expect:
- Python environment setup
- frontend dependency installation
- local API/UI startup
- optional provider API key setup

### 7. Frontend development dependency advisories

The current frontend dependency tree reports:
- `2` moderate vulnerabilities in the Vite/esbuild development stack

These findings are relevant to release hygiene and should be reviewed, but they
do not change the basic fact that the current release is a technical preview
and that the built UI itself remains usable.

### 6. Not yet the prevention framework

Invariant currently delivers:
- testing
- evaluation
- operator workflows
- comparative evidence

It does **not** yet deliver the full production-grade injection prevention
framework described in the broader EchoForgeX direction.

## Support Expectations

Support for the OSS release is currently:
- best effort
- not contractual
- not guaranteed within a defined SLA

Public users should expect:
- documentation
- issue intake
- best-effort review of bugs and feature requests

Public users should **not** expect:
- guaranteed response times
- enterprise support
- custom implementation help as part of the OSS release

## Appropriate Use

This release is appropriate for:
- technical evaluation
- research
- benchmarking
- provider comparison
- internal security exploration
- early integration experiments

This release is not yet ideal for:
- high-assurance enterprise deployment without internal engineering ownership
- claims of complete injection prevention
- relying on the tool as the sole control in a security-critical production system

## Recommended Reading

- [quickstart.md](/Users/jeffreysinason/Development/Invariant/docs/quickstart.md)
- [custom_injection_testing_user_manual.md](/Users/jeffreysinason/Development/Invariant/docs/custom_injection_testing_user_manual.md)
- [public_release_readiness.md](/Users/jeffreysinason/Development/Invariant/docs/public_release_readiness.md)
