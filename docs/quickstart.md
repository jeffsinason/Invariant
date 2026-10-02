# Invariant Quickstart

## Purpose

This guide is the shortest path from cloning the repository to running Invariant
successfully for the first time.

The goal is simple:

An outside technical user should be able to:
- install dependencies
- start the API
- start the UI
- run one case
- run one benchmark
- run one guided custom test

without needing internal project context.

## What You Are Starting

Invariant currently ships as:
- a Python backend harness and API
- a React/Vite operator console

The main UI is the **Invariant Operator Console**.

## Prerequisites

You need:
- `git`
- `python3`
- `node`
- `npm`

You also need a shell environment that can run the commands shown below.

Live provider testing additionally requires one or more API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `MISTRAL_API_KEY`

If you do not have provider keys yet, you can still use the mock provider and
run the product end to end.

## 1. Clone the Repository

```bash
git clone git@github.com:jeffsinason/Invariant.git
cd Invariant
```

## 2. Configure the Python Environment

Create and activate a virtual environment inside `harness`:

```bash
cd harness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cd ..
```

## 3. Configure the Frontend

```bash
cd frontend
npm install
cd ..
```

## 4. Configure Environment Variables

Copy the example environment file:

```bash
cp harness/.env.example harness/.env
```

For mock-only usage, this is enough.

For live providers, edit `harness/.env` and set whichever keys you have:

```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
MISTRAL_API_KEY=your_mistral_key_here
```

If a provider key is missing, that provider’s live flows will not run.

## 5. Start the API

In one terminal:

```bash
cd /path/to/Invariant
make api
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 6. Start the UI

In a second terminal:

```bash
cd /path/to/Invariant
make ui
```

Open:

- [http://127.0.0.1:5173](http://127.0.0.1:5173)

If this is your first frontend run on the machine, install dependencies first:

```bash
make ui-install
```

## 7. First Successful Run: Run Case

In the UI:

1. open `Run Case`
2. choose provider: `mock`
3. choose case: `safe_baseline`
4. run the case

Expected result:
- verdict should be safe

This confirms:
- API is working
- UI is working
- the harness is executing cases
- result display is working

## 8. First Successful Run: Run Benchmark

In the UI:

1. open `Run Benchmark`
2. choose provider: `mock`
3. leave all benchmark cases selected
4. run the benchmark

Expected result:
- `Current Benchmark` fills in with grouped results

This confirms:
- batch execution works
- benchmark storage works
- benchmark UI flow works

## 9. First Successful Run: Guided Custom Test

In the UI:

1. open `Custom Test`
2. choose `guided`
3. choose mode: `evaluated`
4. choose attack family: `Indirect Injection`
5. click `Load Minimal Example`
6. validate
7. run the custom test

Expected result:
- a current custom result appears
- the scenario can be inspected and saved

This confirms:
- custom testing backend works
- template-driven guided mode works
- custom evaluation and result rendering work

## 10. Optional: First Live Provider Run

If you configured a provider key, run a live case from the UI:

1. open `Run Case`
2. choose provider:
   - `openai`, `anthropic`, or `mistral`
3. choose a recommended model
4. run `safe_baseline`

Expected result:
- a normal safe response from the live provider

Start with `safe_baseline` before running injection cases.

## Common Problems

### API port already in use

Check:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

If needed, stop the old process and restart `make api`.

### UI port already in use

Check:

```bash
lsof -nP -iTCP:5173 -sTCP:LISTEN
```

Then restart `make ui`.

### Provider does not work

Check:
- the API key is set in `harness/.env`
- the API was restarted after editing `.env`
- the selected model belongs to that provider

### A model list looks incomplete

By default the UI shows recommended harness models.

Use:
- `Show all available models`

to expose the full discovered provider list.

## Useful Commands

Backend tests:

```bash
make test
```

Frontend tests:

```bash
cd frontend
npm test
```

Frontend build:

```bash
cd frontend
npm run build
```

Live provider matrix:

```bash
make live-matrix
```

## Where To Go Next

After the quickstart succeeds, use these documents:

- [custom_injection_testing_user_manual.md](custom_injection_testing_user_manual.md)
- [live_testing_workflow.md](live_testing_workflow.md)
- [benchmark_execution_workflow.md](benchmark_execution_workflow.md)
- [frontend_architecture.md](frontend_architecture.md)
