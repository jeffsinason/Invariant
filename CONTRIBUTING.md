# Contributing to Invariant

## Purpose

This document explains how to contribute to Invariant as an open source
EchoForgeX project.

Invariant is a technical security tool. Contributions should improve:
- correctness
- clarity
- usability
- reproducibility
- trust-boundary rigor

## Contribution Priorities

The most useful contributions are usually in these areas:

1. benchmark case quality
2. evaluator correctness
3. provider integrations
4. UI clarity and workflow quality
5. documentation and first-run usability
6. automated test coverage

## Before You Start

Before making a substantial change:
- read the README
- review relevant docs in `docs/`
- check existing issues if they exist
- understand whether the change affects:
  - canonical benchmarks
  - custom testing
  - UI workflows
  - provider behavior

If the change is large, open an issue first instead of sending a large surprise
pull request.

## Scope

### In Scope

- bug fixes
- test improvements
- documentation improvements
- UI usability improvements
- provider integration improvements
- benchmark and evaluator improvements
- safe, well-scoped feature work aligned with the roadmap

### Out of Scope Without Prior Discussion

- large architectural rewrites
- major license or governance changes
- changes that weaken benchmark rigor
- removal of structured evaluation behavior
- product repositioning away from the EchoForgeX project direction

## Development Expectations

Contributions should:
- match the existing project structure
- stay closely scoped to the problem being solved
- avoid unrelated refactors
- include tests where practical
- preserve or improve documentation when behavior changes

## Tests

Before submitting a pull request, run what is relevant:

Backend:

```bash
harness/.venv/bin/python -m unittest discover -s harness/tests -v
```

Frontend:

```bash
cd frontend
npm test
npm run build
```

If you cannot run part of the suite, say so clearly in the pull request.

## Pull Requests

Good pull requests should:
- explain the problem
- explain the change
- explain any tradeoffs
- mention updated docs or tests
- stay narrow enough to review

Include screenshots for UI changes when helpful.

## Canonical Benchmarks vs Custom Tests

Invariant distinguishes between:
- canonical benchmark cases
- user-authored custom tests

Changes to canonical benchmarks should be especially careful because they affect
comparability and project-controlled evaluation behavior over time.

## Security Issues

Do not open a public issue for a sensitive security disclosure.

See:
- [SECURITY.md](/Users/jeffreysinason/Development/Invariant/SECURITY.md)

## License

By contributing to this repository, you agree that your contributions are made
under the repository’s Apache License 2.0 terms unless explicitly agreed
otherwise in writing.
