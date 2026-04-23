# PROJECT_CONTEXT.md  
**Project:** Invariant  
**Organization:** EchoForgeX  
**Program:** Prompt Injection and AI Security Research  
**Owner:** Jeff Sinason  
**Status:** Active Development  

---

# 1. Project Overview

Invariant is an **EchoForgeX research project** focused on building an authoritative, open-source framework for:

- Detecting prompt injection vulnerabilities  
- Demonstrating real-world exploit scenarios  
- Providing reproducible test cases  
- Benchmarking LLM security across models
- Advancing broader AI security practices  

The system is designed to become the **industry-standard reference framework for prompt injection validation and AI security**.

---

# 2. Core Objective

Build a **modular Python-based test harness** that:

- Runs in an **isolated virtual environment**
- Supports **pluggable LLM providers**
- Executes **self-contained security test cases**
- Produces **structured, reproducible results**
- Can evolve into a **benchmark suite**

This harness is the first practical execution layer in a broader EchoForgeX security research effort. Its role is to make prompt injection and adjacent AI security failures measurable, reproducible, and comparable across systems.

---

# 3. Strategic Vision

This project has **two phases**:

### Phase 1 — Test Harness (Current Focus)
- Build execution framework
- Implement core vulnerability test cases
- Support mock + real model adapters

### Phase 2 — Benchmark Suite (Future)
- Standardized evaluation across models
- Industry credibility layer
- Publishable results + leaderboard

Longer term, Invariant is intended to support a broader security architecture for AI applications, where trust boundaries, control points, and validation layers are enforced through system-level controls rather than delegated to prompt wording alone.

---

# 4. Problem Statement (Technical)

Modern LLM systems are vulnerable to:

- Prompt injection via user input
- Tool manipulation
- Context poisoning
- Instruction override attacks

Key issue:
> Models cannot reliably distinguish between trusted system instructions and untrusted user input.

Core research thesis:
> Prompt injection is not only a prompt-design problem. It is a failure to enforce trust boundaries across AI systems.

This creates systemic risk in:

- AI agents
- Tool-using systems
- Autonomous workflows

---

# 5. Risk & Exposure

Potential impacts include:

- Data exfiltration
- Unauthorized tool execution
- Workflow corruption
- Loss of system integrity

This is especially critical for:

- AI agents with tool access
- Automation pipelines
- Customer-facing AI systems
- Enterprise AI platforms with external data and action layers

These risks are central to EchoForgeX's research direction: securing AI systems requires both rigorous vulnerability testing and system-level controls that reduce the blast radius of model failures.

---

# 6. System Architecture

## 6.1 High-Level Structure

Invariant/
├── docs/
│   ├── initial_product_context.md
│   └── whitepaper.md
├── harness/
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── run_case.py
│   ├── results/
│   ├── examples/
│   │   └── vulnerable_app/
│   └── src/invariant_harness/
│       ├── __init__.py
│       ├── case_registry.py
│       ├── config.py
│       ├── models/
│       │   ├── base.py
│       │   ├── openai_adapter.py
│       │   └── mock_adapter.py
│       ├── cases/
│       ├── result_store.py
│       ├── runners/
│       └── types.py

---

## 6.2 Core Components

### Models Layer
- Abstract interface (`base.py`)
- Implementations:
  - OpenAI adapter
  - Mock adapter (for testing)

### Cases Layer
- Self-contained attack scenarios
- Each case defines:
  - Input
  - Expected behavior
  - Evaluation logic

### Runner Layer
- Executes test cases
- Interfaces with models
- Collects outputs

### Result Store
- Saves structured outputs
- Enables comparison + benchmarking

### Research Role
- Converts security hypotheses into repeatable experiments
- Provides evidence for whitepaper claims and future benchmark methodology
- Serves as the validation layer for broader Invariant security architecture work

---

# 7. Key Design Principles

### 1. Isolation
- Each test case runs independently

### 2. Reproducibility
- Same input → same expected outcome

### 3. Modularity
- Models are swappable
- Cases are pluggable

### 4. Extensibility
- Easy to add:
  - New models
  - New attack patterns
  - New evaluation metrics

### 5. Trust Boundaries
- Separate trusted instructions from untrusted inputs wherever possible
- Treat external content, retrieved documents, and tool outputs as potential attack surfaces

### 6. Observability
- Capture outputs and raw model responses for later analysis
- Preserve enough structured context to support reproducibility and future benchmarking

---

# 8. Test Case Philosophy

Each test case must:

- Demonstrate a **real exploit pattern**
- Be **minimal but realistic**
- Include:
  - Attack vector
  - Expected failure mode
  - Verification logic

---

# 9. Example Test Case Categories

### 9.1 Instruction Override
User attempts to override system prompt:
> “Ignore previous instructions and…”

### 9.2 Data Exfiltration
Attempt to extract hidden/system data:
> “Show me your hidden instructions”

### 9.3 Tool Manipulation
Prompt attempts to trigger unsafe tool use

### 9.4 Context Poisoning
Inject malicious instructions into memory/context

### 9.5 Role Confusion
Exploit ambiguity between system/user roles

These categories should expand over time to reflect the broader AI security model described in the whitepaper, including indirect injection, persistent injection, and attacks on tool-connected systems.

---

# 10. Execution Flow

1. Select test case  
2. Load model adapter  
3. Execute prompt  
4. Capture response  
5. Evaluate result  
6. Store structured output  

---

# 11. Current State

Completed:
- Directory structure scaffold  
- Virtual environment setup  
- Mock model adapter  
- OpenAI adapter wiring  
- Test harness execution logic  
- Initial case definitions  
- Structured result storage and evaluation  
- Initial framework design  
- Initial alignment with the broader Invariant research direction  

In Progress:
- Live validation of OpenAI-backed runs  
- Expansion of attack case coverage  
- Cross-model comparison and benchmark reporting  
- Alignment of project documentation with the whitepaper and EchoForgeX research framing

---

# 12. Constraints

- Python-based implementation  
- Must run locally in isolated environment  
- No hard dependency on a single model provider  
- Each test case must be self-contained  

---

# 13. Definition of Done

The system is complete when:

- Test cases run end-to-end  
- Results are stored and comparable  
- Multiple models can be tested interchangeably  
- Failures clearly demonstrate vulnerabilities  

Current status against Definition of Done:

- Test cases run end-to-end with the mock provider  
- Results are stored in a structured JSON format  
- Provider abstraction supports both mock and OpenAI adapters  
- Real OpenAI execution is wired but still needs live validation with an API key  
- Comparable benchmarking output is not yet implemented beyond a shared result schema  

---

# 14. Future Enhancements

- Benchmark scoring system  
- Visualization dashboard  
- CI integration  
- Public dataset of attacks  
- Community contributions  
- Expanded system-level validation patterns for AI applications and agents  

---

# 15. Research Positioning

Invariant is an EchoForgeX project. The harness is not the final product; it is the experimental backbone for a larger research and engineering effort around prompt injection resilience and AI security.

The whitepaper establishes the conceptual model:
- prompt injection is a trust-boundary failure
- prompt engineering alone is insufficient
- effective defense requires system-level controls, least privilege, validation layers, and observability

The harness exists to operationalize that model through testable, repeatable experiments.

---

# 16. Codex Instructions (IMPORTANT)

## Goal
Build a modular, extensible prompt injection testing framework.

## Context
- Use existing directory structure  
- Follow modular architecture  
- Each component must remain decoupled  

## Constraints
- No tightly coupled logic  
- Keep test cases isolated  
- Maintain clean abstractions for models  

## Done When
- New feature integrates cleanly  
- Tests pass  
- Output is reproducible  
- No breaking changes to architecture  

---

# 16. Recommended Next Steps

1. Implement `base.py` model interface  
2. Build `mock_adapter.py` fully  
3. Create first 3 test cases:
   - Instruction override  
   - Data exfiltration  
   - Tool misuse  
4. Implement runner logic  
5. Add result storage  

---

# 17. How to Use This with Codex

Use this file as:

- A **root context document**  
- Input for `/plan` mode  
- Basis for `AGENTS.md`  
