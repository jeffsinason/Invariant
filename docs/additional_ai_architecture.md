# Additional AI Architecture

## Purpose

This document explains how additional AI systems and models can be incorporated into Invariant as the project evolves from a test harness into a broader AI security framework.

Invariant is an EchoForgeX project. Its long-term goal is not only to benchmark model behavior, but to help build and protect AI systems against prompt injection and related security failures.

## Why This Matters

As the project grows, "additional AI" can mean different things:
- more providers under test
- more AI components inside the system being protected
- more AI components used to strengthen the protective framework itself

Those roles should be kept distinct.

If they are not kept distinct, it becomes difficult to answer basic questions such as:
- which model is being tested
- which model is making a security decision
- which model is merely part of the protected application

## Three Ways Additional AI Fits Into Invariant

### 1. Additional Target Providers

This is the most immediate and simplest extension.

In this mode, additional AI means adding more model providers or model families for the harness to test.

Examples:
- Google-hosted models
- Mistral-hosted models
- Cohere-hosted models
- local or open-weight models
- Azure-hosted variants
- Bedrock-hosted variants

In architecture terms, these are **models under test**.

They should integrate through:
- a provider adapter
- normalized request and response mapping
- benchmark compatibility
- provider comparison support

This is the direct continuation of the current OpenAI and Anthropic integration model.

### 2. AI Inside the Protected System

In this mode, additional AI refers to the actual AI-powered application that Invariant is trying to evaluate or protect.

Examples:
- a RAG assistant
- a tool-using agent
- a workflow automation assistant
- a multi-agent application
- a customer-facing AI system with retrieval and actions

In these systems, multiple AI components may already exist:
- a summarizer
- a router
- a retrieval assistant
- a planning model
- a tool-selection model

Invariant should eventually be able to test these systems as composed architectures rather than only as isolated model calls.

### 3. AI Used in the Security Control Plane

In this mode, additional AI is used as part of the defensive framework itself.

Examples:
- risk classification models
- content screening models
- retrieval sanitization models
- output validation models
- tool-call review models

These are not the models under test. These are **control-plane AI components**.

They may help with:
- scoring risk
- classifying trust level
- detecting suspicious instructions
- validating outputs before release

However, these should support deterministic security controls rather than replace them.

## Architectural Separation

The framework should distinguish between:

### Models Under Test

These are the target systems whose security behavior is being measured.

Examples:
- OpenAI
- Anthropic
- future provider adapters

### Application AI Components

These are AI components inside the protected application.

Examples:
- retriever assistant
- planner
- summarizer
- tool selector

### Control-Plane AI Components

These are optional AI systems used to strengthen the framework.

Examples:
- risk classifier
- validator
- policy assistant

### Deterministic Controls

These remain the non-AI enforcement layer:
- permission boundaries
- allowlists
- tool authorization
- trust assignment
- output schemas
- explicit validators

This separation is important because AI should assist the framework without becoming the only security boundary.

## Design Recommendation

The system should eventually use explicit component roles such as:

- `model_under_test`
- `application_component`
- `control_component`

Or, if a more general label is preferred:

- `target_model`
- `system_model`
- `security_model`

That role distinction should carry through:
- backend APIs
- stored metadata
- benchmark reports
- comparison views

## Near-Term Recommendation

In the near term, additional AI should be added mainly as:

1. **new target providers**
2. **new system configurations to test**

This preserves the clarity of the current harness and makes the benchmark suite stronger.

## Medium-Term Recommendation

As Invariant moves toward a protective framework, additional AI can be introduced into the control plane for:
- classification
- validation
- content screening
- tool-call review

But these should remain advisory or secondary to deterministic enforcement.

## Long-Term Recommendation

The long-term evolution should be:

1. benchmark individual providers
2. benchmark composed AI systems
3. build a security framework that governs trust boundaries across those systems

At that stage, Invariant will no longer be only a model evaluation harness. It will be a framework for securing AI applications made of multiple interacting AI and non-AI components.

## Relationship to the Front-End

The future front-end should be designed with this growth path in mind.

That means it should eventually support concepts like:
- provider under test
- system configuration
- component role
- control-plane validation layers

This will make the front-end useful not only for running single attacks, but also for inspecting the behavior of full AI system architectures.

## Summary

Additional AI can be incorporated into Invariant in three ways:

1. as more providers under test
2. as AI components within the system being protected
3. as AI components in the security control plane

The architecture should keep those roles distinct so the framework remains understandable, testable, and defensible as it grows.
