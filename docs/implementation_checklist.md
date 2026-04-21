# Invariant Implementation Checklist

This checklist tracks the next development steps for the Invariant harness and case roadmap.

## Provider Support

- [x] Mock provider adapter
- [x] OpenAI provider adapter
- [x] Anthropic provider adapter
- [x] OpenAI live validation for `direct_override`
- [x] OpenAI live validation for `prompt_leakage`
- [x] Anthropic live validation for `direct_override`
- [x] Anthropic live validation for `prompt_leakage`
- [x] Shared result schema for `raw_response`
- [x] Shared result schema for `request_id`
- [x] Shared result schema for `stop_reason`
- [x] Shared result schema for `usage`
- [x] Persist structured provider error metadata in saved results

## Current Case Logic

- [x] `direct_override`
- [x] `prompt_leakage`
- [x] Fix false-positive prompt leakage evaluation for safe refusals
- [x] Add `safe_baseline`
- [x] Add `role_confusion`
- [x] Add `obfuscated_injection`

## Retrieval and Content Cases

- [x] Define retrieval-content fixture format
- [x] Add `indirect_injection`
- [x] Add content-ingestion simulation in the harness

## Tool and Agent Cases

- [x] Define simulated tool interface for test cases
- [x] Add tool-call logging to saved results
- [x] Add `tool_manipulation`
- [x] Add `data_exfiltration_tool_use`
- [x] Add `unauthorized_action_execution`

## Session and Memory Cases

- [x] Define multi-turn conversation fixture format
- [x] Add session-state support in the harness
- [x] Add `context_poisoning`
- [x] Add `persistent_injection`
- [x] Add `contextual_injection`

## Benchmark and Comparison

- [x] Add batch case runner
- [x] Add result normalization for provider comparison
- [x] Add provider comparison report format
- [x] Add `benchmark_matrix`

## Testing

- [x] Add unit tests for adapter mapping
- [x] Add unit tests for case evaluation logic
- [x] Add serialization tests for saved result JSON
- [x] Add integration tests gated by `OPENAI_API_KEY`
- [x] Add integration tests gated by `ANTHROPIC_API_KEY`

## Documentation

- [x] Update product context to reflect current package layout
- [x] Align terminology between the whitepaper and product context
- [x] Create canonical case roadmap
- [x] Document live testing workflow for all providers
- [x] Document benchmark execution workflow
