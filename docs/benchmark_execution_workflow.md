# Benchmark Execution Workflow

This document describes how to run the Invariant benchmark matrix and interpret the output.

## Benchmark Entry Point

Use [run_benchmark.py](/Users/jeffreysinason/Development/Invariant/harness/run_benchmark.py) from [harness](/Users/jeffreysinason/Development/Invariant/harness):

```bash
python3 run_benchmark.py --provider mock --cases all
```

You can target a subset of cases:

```bash
python3 run_benchmark.py --provider openai --cases safe_baseline,direct_override,prompt_leakage
python3 run_benchmark.py --provider anthropic --cases safe_baseline,direct_override,prompt_leakage
```

## What the Benchmark Matrix Does

The benchmark matrix:
- runs multiple harness cases in one batch
- normalizes the results into a comparable schema
- summarizes total, safe, and vulnerable cases
- optionally saves both per-case results and a benchmark report JSON

## Report Contents

Saved benchmark reports include:
- `report_type`
- `provider`
- `model_name`
- `generated_at_utc`
- summary counts
- normalized per-case result entries

Normalized entries include:
- `case_name`
- `provider`
- `model_name`
- `vulnerable`
- `response_text`
- `request_id`
- `stop_reason`
- `usage`
- `tool_call_count`
- `tool_call_names`
- `timestamp_utc`

## Suggested Benchmark Baseline

A practical first benchmark set is:

```text
safe_baseline
direct_override
prompt_leakage
role_confusion
obfuscated_injection
indirect_injection
tool_manipulation
data_exfiltration_tool_use
unauthorized_action_execution
context_poisoning
persistent_injection
contextual_injection
```

## Recommended Provider Comparison Flow

1. Run the same case set against OpenAI
2. Run the same case set against Anthropic
3. Compare:
   - vulnerable case count
   - response patterns
   - tool call behavior
   - usage differences
4. Preserve raw provider payloads for deeper inspection when verdicts differ

## Testing the Benchmark Layer

The benchmark and batch-runner logic are covered by the automated test suite:

```bash
.venv/bin/python -m unittest discover -s tests -v
```
