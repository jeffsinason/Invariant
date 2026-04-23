# Live Testing Workflow

This document describes how to run Invariant against live providers.

## Prerequisites

From [harness/.env.example](/Users/jeffreysinason/Development/Invariant/harness/.env.example), configure:

```env
MODEL_PROVIDER=mock
MODEL_NAME=
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

You can keep `MODEL_PROVIDER=mock` and select live providers explicitly with `--provider`.

## Run Individual Cases

From [harness](/Users/jeffreysinason/Development/Invariant/harness):

```bash
python3 run_case.py direct_override --provider openai
python3 run_case.py prompt_leakage --provider openai

python3 run_case.py direct_override --provider anthropic
python3 run_case.py prompt_leakage --provider anthropic
```

You can also exercise the broader suite:

```bash
python3 run_case.py safe_baseline --provider openai --no-save
python3 run_case.py role_confusion --provider anthropic --no-save
python3 run_case.py indirect_injection --provider openai --no-save
python3 run_case.py tool_manipulation --provider anthropic --no-save
```

## Expected Output Shape

Each run prints:
- `case_name`
- `provider`
- `model_name`
- `vulnerable`
- `response`
- `notes`
- optional `request_id`
- optional `stop_reason`
- optional `usage`
- optional `tool_calls`
- `timestamp`
- `saved_to` when saving is enabled

## Saved Results

Successful runs are saved to [harness/results](/Users/jeffreysinason/Development/Invariant/harness/results) as JSON.

Saved results include:
- normalized top-level case metadata
- provider and model identifiers
- vulnerability verdict
- raw provider response
- request metadata
- usage metadata
- tool-call metadata when applicable

If a run fails before a response is produced and saving is enabled, the harness also writes a structured error result containing:
- `error_type`
- `error_message`

## Running the Automated Test Suite

To run the local test suite:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Live integration tests are env-gated:
- OpenAI tests run only when `OPENAI_API_KEY` is present
- Anthropic tests run only when `ANTHROPIC_API_KEY` is present

## Recommended Live Validation Order

1. `safe_baseline`
2. `direct_override`
3. `prompt_leakage`
4. `indirect_injection`
5. tool-related cases
6. session and memory cases

That order gives you a clean progression from control cases to higher-complexity attack simulations.
