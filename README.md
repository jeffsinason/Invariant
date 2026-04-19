# Invariant

**A system-level security framework for enforcing trust boundaries in AI applications.**

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

## 🚀 Roadmap

- Define core interfaces  
- Build reference implementation  
- Add adversarial testing suite  
- Integrate with major LLM providers  

---

## 📄 Whitepaper

See /docs/whitepaper.md for full details.
