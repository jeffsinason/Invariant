# Invariant

**A system-level security framework for enforcing trust boundaries in AI applications.**

**Current release:** `0.1.0-alpha`  
**Release posture:** public technical preview

---

## 🚨 The Problem

Prompt injection is not a prompt problem.

It is a failure to enforce invariants.

- User input overrides system intent  
- Untrusted data becomes executable instruction  
- Models trigger actions they should not control  

Organizations like OWASP and NIST have identified this as a critical risk class.

---

## 🎯 The Solution

Invariant defines and enforces **non-negotiable rules** for AI systems:

> Things that must always be true, no matter what the model sees.

Instead of trying to fix prompts, Invariant secures the system around them.

## What This Release Delivers

This technical preview delivers:
- a prompt injection and trust-boundary test harness
- a browser-based operator console
- canonical benchmark execution
- guided and advanced custom injection testing
- saved artifacts for runs, benchmarks, and custom scenarios

This release does **not** yet deliver the full injection prevention framework.
It is the testing and operator-facing surface for that broader EchoForgeX
direction.

---

## 🧩 Core Idea

Every AI system should enforce invariants such as:

- User input cannot override system instructions  
- Untrusted data cannot trigger privileged actions  
- Tool usage must be explicitly authorized  
- Outputs must conform to defined structure  

Invariant provides the architecture to enforce these rules.

---

## 🏗️ Reference Architecture

[User Input]
     ↓
[Risk Classifier]
     ↓
[Trust-Aware Context Builder]
     ↓
[LLM (Constrained)]
     ↓
[Tool Gateway (Permissioned)]
     ↓
[Validator]
     ↓
[Output]

---

## 🔐 Framework Components

- Input Classification Engine  
- Context Builder  
- Execution Orchestrator  
- Policy Engine  
- Output Validator  
- Observability Layer  

---

## License

This repository is licensed under the Apache License 2.0.

See:
- [LICENSE](LICENSE)
- [CHANGELOG.md](CHANGELOG.md)

---

## OSS, IP, and Branding

Invariant is an EchoForgeX project released as open source software.

The intent of this repository is to distribute the harness and operator console
openly while supporting the larger EchoForgeX injection prevention framework
direction.

For a short explanation of the OSS, IP, and branding posture, see:
- [oss_ip_and_branding.md](docs/oss_ip_and_branding.md)

For repository governance and reporting, see:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)

Current release posture:
- `0.1.0-alpha`
- public technical preview

---

## Quickstart

Start here:
- [quickstart.md](docs/quickstart.md)

Short version:

```bash
git clone git@github.com:jeffsinason/Invariant.git
cd Invariant
cd harness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cd ../frontend
npm install
cd ..
cp harness/.env.example harness/.env
make api
make ui
```

Then open:
- [http://127.0.0.1:5173](http://127.0.0.1:5173)

For a first end-to-end run without API keys:
- use provider `mock`
- run `safe_baseline` from `Run Case`

For release boundaries and support expectations, see:
- [support_and_limitations.md](docs/support_and_limitations.md)

---

## UI Preview

Run case workflow:

![Invariant Run Case](docs/assets/invariant-console-run-case.png)

Run benchmark workflow:

![Invariant Run Benchmark](docs/assets/invariant-console-run-benchmark.png)

Custom injection testing workflow:

![Invariant Custom Test](docs/assets/invariant-console-custom-test.png)

Artifact comparison workflow:

![Invariant Artifacts](docs/assets/invariant-console-artifacts.png)

---

## Running and Testing

Primary workflows:
- `Run Case` for a single canonical test
- `Run Benchmark` for provider and family comparison
- `Custom Test` for guided or advanced scenario authoring
- `Artifacts` for saved run, benchmark, and comparison review

Run the full local test suite:

```bash
make test
```

or:

```bash
bash scripts/test.sh
```

Run a mock benchmark matrix:

```bash
make benchmark-mock
```

Run the live provider matrix:

```bash
make live-matrix
```

Run the Phase 2 backend API:

```bash
make api
```

Run the Phase 2 operator console:

```bash
make ui-install
make ui
```

Run the frontend test suite:

```bash
cd frontend
npm test
```

Known frontend release-hygiene note:
- `npm audit` currently reports `2` moderate vulnerabilities in the Vite/esbuild
  dev-server toolchain
- these affect development tooling posture, not the built static assets
- they should still be reviewed before broader public attention

The live matrix script will:
- run core and extended cases against OpenAI when `OPENAI_API_KEY` is available
- run core and extended cases against Anthropic when `ANTHROPIC_API_KEY` is available
- run core and extended cases against Mistral when `MISTRAL_API_KEY` is available
- save benchmark artifacts in [harness/results](harness/results)

The API currently exposes:
- `GET /health`
- `GET /providers`
- `GET /models`
- `GET /cases`
- `POST /runs/case`
- `POST /runs/benchmark`
- `GET /runs`
- `GET /runs/{artifact_name}`
- `GET /benchmarks`
- `GET /benchmarks/{artifact_name}`

The Phase 2 front-end lives in [frontend](frontend) and uses:
- React + TypeScript + Vite
- the FastAPI backend in [api.py](harness/src/invariant_harness/api.py)

Start the full local Phase 2 stack in two terminals:

```bash
make api
make ui-install
make ui
```

Then open:
- [http://127.0.0.1:5173](http://127.0.0.1:5173)

Current front-end workflows:
- run a single case from the `Run Case` tab
- run a benchmark and compare the current benchmark to a selected saved benchmark from the `Run Benchmark` tab
- build and run guided or advanced custom injection scenarios from the `Custom Test` tab
- compare run artifacts, benchmark artifacts, and provider differences from the `Artifacts` tab
- review operator summaries first, then expand into technical metadata and raw payloads when needed

Current front-end layout:
- `Invariant Operator Console` header
- `Run Case` tab:
  - run controls
  - `Current Run Case`
  - `Selected Case Result` with saved-run selector
- `Run Benchmark` tab:
  - compact benchmark run control
  - `Current Benchmark Controls` and `Selected Benchmark Controls`
  - side-by-side `Current Benchmark` and `Selected Benchmark` panels
- `Custom Test` tab:
  - guided and advanced scenario authoring modes
  - current custom result
  - saved scenario selection
  - saved custom run and run-group inspection
  - saved custom run and run-group comparison
- `Artifacts` tab:
  - `Run Comparison`
  - `Benchmark Comparison`
  - `Provider Differences`

Benchmark workflow:
- run a new benchmark from the compact top control
- inspect the most recent benchmark from the current session in `Current Benchmark`
- select any saved benchmark independently in `Selected Benchmark`
- filter both benchmark panels by family and sort order without changing the other panel

Artifact drilldown behavior:
- case results show an operator summary first, followed by expandable technical metadata and raw provider payloads
- benchmark results show grouped family summaries and detailed case rows before raw benchmark JSON

Current retrieval benchmark labels:
- `direct_obedience`
- `unsafe_repetition`
- `safe_summary`
- `safe_refusal`
- `safe_other`

For setup and workflow details, see:
- [quickstart.md](docs/quickstart.md)
- [live_testing_workflow.md](docs/live_testing_workflow.md)
- [benchmark_execution_workflow.md](docs/benchmark_execution_workflow.md)
- [frontend_architecture.md](docs/frontend_architecture.md)
- [custom_injection_testing_user_manual.md](docs/custom_injection_testing_user_manual.md)
- [support_and_limitations.md](docs/support_and_limitations.md)
- [public_release_readiness.md](docs/public_release_readiness.md)

---

## 📄 Whitepaper

See /docs/whitepaper.md for full details.
