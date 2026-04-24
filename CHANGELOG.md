# Changelog

All notable changes to Invariant should be tracked in this file.

The project currently follows a pre-1.0 release posture.

## [0.1.0-alpha] - 2026-04-23

### Added

- canonical prompt injection and trust-boundary benchmark suite
- provider support for:
  - OpenAI
  - Anthropic
  - Mistral
  - mock provider
- normalized benchmark execution and saved result artifacts
- FastAPI backend for case, benchmark, and custom-test execution
- React/Vite operator console with tabs for:
  - `Run Case`
  - `Run Benchmark`
  - `Custom Test`
  - `Artifacts`
- guided and advanced custom injection testing workflows
- custom scenario save/load, run, and run-group support
- template-driven custom testing catalog
- dedicated custom injection testing user documentation
- public OSS licensing and governance scaffolding:
  - Apache-2.0 license
  - contributing guide
  - security policy
  - issue templates
- public quickstart documentation
- UI screenshots and product icon

### Notes

- this is a public technical preview / alpha release
- the harness and operator console are usable now
- the broader injection prevention framework is not yet part of the released OSS implementation
