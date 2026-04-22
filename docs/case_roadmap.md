# Invariant Case Roadmap

This roadmap defines the canonical security test cases for the Invariant harness.

It is intended to keep case planning consistent across:
- threat modeling
- harness development
- provider validation
- future benchmark reporting

Invariant is an EchoForgeX project. These cases are designed to support both prompt injection validation and broader AI security research.

## Canonical Cases

| Case Name | Threat Class | Required Harness Capability | Current Readiness |
| --- | --- | --- | --- |
| `safe_baseline` | Control / Non-attack Baseline | Benign prompt execution, expected-safe response validation | Can be tested now |
| `direct_override` | Direct Injection / Instruction Override | Single-turn prompt execution, provider adapter, response capture, rule-based evaluation | Can be tested now |
| `prompt_leakage` | Prompt Leakage / Data Exposure | Single-turn prompt execution, response capture, leak-vs-refusal evaluation | Can be tested now |
| `role_confusion` | Role Confusion | Support for multi-role message construction and role-boundary evaluation | Can be tested now, but benefits from richer multi-message harness support |
| `obfuscated_injection` | Obfuscated Injection | Variant generation or fixture library for encoded, multilingual, or transformed attacks | Partially testable now; stronger coverage needs a fixture library |
| `indirect_injection` | Indirect Injection | Ability to simulate retrieved or untrusted external content being merged into model context | Needs retrieval or content-ingestion infrastructure |
| `indirect_injection_hidden_metadata` | Indirect Injection | Ability to simulate malicious instructions hidden in metadata or operator notes | Can be tested now |
| `indirect_injection_priority_conflict` | Indirect Injection | Ability to simulate retrieved content that falsely claims higher authority than the user task | Can be tested now |
| `indirect_injection_cross_document` | Indirect Injection | Ability to simulate one poisoned document competing with multiple benign documents | Can be tested now |
| `indirect_injection_html_comment` | Indirect Injection | Ability to simulate retrieved content that hides instructions in comments or metadata | Can be tested now |
| `tool_manipulation` | Tool Manipulation | Tool schema support, tool-call capture, prompt-to-tool routing visibility | Needs tool or agent infrastructure |
| `tool_manipulation_policy_bypass` | Tool Manipulation | Tool schema support plus social-engineering or policy-bypass prompts around authorization boundaries | Can be tested now |
| `data_exfiltration_tool_use` | Data Exfiltration / Tool Abuse | Tool-call simulation, protected data fixture, tool invocation logging, output validation | Needs tool or agent infrastructure |
| `unauthorized_action_execution` | Unauthorized Action / Tool Manipulation | Action tool simulation, side-effect logging, allow or deny policy checks | Needs tool or agent infrastructure |
| `context_poisoning` | Context Poisoning | Multi-turn or session state, memory store or carried context, cross-turn evaluation | Needs agent or session infrastructure |
| `persistent_injection` | Persistent Injection | Saved memory, history, or document store plus session restart or reload behavior | Needs agent or session infrastructure |
| `contextual_injection` | Contextual Injection | Multi-turn conversations, prior-turn carryover, state-aware evaluation | Needs agent or session infrastructure |
| `delayed_trigger_injection` | Contextual Injection / Delayed Trigger | Multi-turn conversations with a planted trigger phrase that activates later | Can be tested now |
| `benchmark_matrix` | Benchmarking / Comparative Evaluation | Batch runner, result normalization, cross-provider comparison, reporting | Partially testable now; full version needs a reporting layer |

## Recommended Implementation Order

1. `safe_baseline`
2. `direct_override`
3. `prompt_leakage`
4. `role_confusion`
5. `obfuscated_injection`
6. `indirect_injection`
7. `tool_manipulation`
8. `data_exfiltration_tool_use`
9. `unauthorized_action_execution`
10. `context_poisoning`
11. `persistent_injection`
12. `contextual_injection`
13. `benchmark_matrix`

## Current Harness Coverage

Available now:
- single-turn provider execution
- live OpenAI and Anthropic provider testing
- structured result saving
- basic rule-based evaluation

Still needed for the next class of cases:
- retrieval or content-ingestion simulation
- multi-turn or session state
- tool-call simulation and logging
- batch comparison and reporting

## Notes

- `safe_baseline` is important as a control case and should be treated as part of the canonical suite.
- `benchmark_matrix` is not an attack pattern. It is a benchmark execution mode that becomes meaningful once multiple cases and providers are normalized under a shared result schema.
- Cases should remain self-contained wherever possible, with infrastructure added only when the threat class requires it.

## Depth Gaps

The current suite is broad, but many cases are still shallow in one important sense: they are single-fixture passes that often reward refusal behavior without yet stressing the model through enough realistic variation.

The next depth improvements should focus on:
- multiple prompt variants per case
- stronger indirect and retrieval-borne attack fixtures
- more realistic tool abuse attempts
- cross-turn persistence and delayed-trigger behavior
- stronger success criteria than simple refusal or non-refusal patterns

The goal is not only to have cases that execute. It is to have cases that meaningfully separate stronger and weaker security behavior across providers and over time.
