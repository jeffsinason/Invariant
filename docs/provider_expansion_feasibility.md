# Provider Expansion Feasibility

## Purpose

This document evaluates the next provider candidates for Invariant after the
current release hardening pass.

The current provider set already includes:
- OpenAI
- Anthropic
- Mistral
- mock provider

This document evaluates:
- Google Gemini
- xAI Grok
- Cohere
- open-source / open-weight options

The goal is not to implement all three immediately.

The goal is to determine:
- technical feasibility
- adapter fit
- likely release value
- recommended implementation order

## Evaluation Criteria

Each provider is evaluated against:

1. official API maturity
2. official SDK maturity
3. model discovery support
4. request/response mapping fit
5. likely UI integration complexity
6. likely benchmark value
7. likely maintenance risk

## 1. Google Gemini

### Official API posture

Google provides the official Gemini API and recommends the Google GenAI SDK.
Sources:
- [Gemini API docs](https://ai.google.dev/docs)
- [Google GenAI SDK migration guide](https://ai.google.dev/gemini-api/docs/migrate)

### SDK and request surface

The recommended Python path is the Google GenAI SDK.

The documented Python shape is approximately:
- `from google import genai`
- `client.models.generate_content(...)`

This is a clean adapter target for Invariant.

### Model discovery

The Gemini API supports model-oriented workflows and has official API
reference material around model usage and content generation. The SDK/API shape
appears mature enough for model selection workflows. Source:
- [Gemini API docs](https://ai.google.dev/docs)

### Fit with current harness

Good fit.

Why:
- current harness already maps well to “generate content” style requests
- provider/model abstraction already exists
- the current UI model-picker flow can absorb another modern provider

### Likely complexity

Moderate.

Most work will be:
- adapter implementation
- model registry integration
- env var handling
- response normalization
- testing

### Benchmark value

High.

Gemini adds:
- a major additional model family
- broader comparative value across mainstream providers
- stronger credibility for public technical preview

### Maintenance risk

Moderate.

Google APIs evolve, but Gemini is a major strategic platform and the official
SDK path is clear.

### Recommendation

**Strong next candidate.**

If one additional provider is added soon, Gemini should be first.

## 2. xAI Grok

### Official API posture

xAI provides official API documentation, including chat and response-style
surfaces plus model listing.
Sources:
- [xAI docs overview](https://docs.x.ai/docs)
- [xAI chat / responses API reference](https://docs.x.ai/docs/api-reference)
- [xAI models endpoint](https://docs.x.ai/developers/rest-api-reference/inference/models)

### SDK and request surface

xAI exposes:
- `/v1/chat/completions`
- `/v1/responses`
- model listing

This is enough for adapter work.

### Model discovery

Yes. Official model-list support exists. Source:
- [xAI models endpoint](https://docs.x.ai/developers/rest-api-reference/inference/models)

### Fit with current harness

Good enough.

The response-oriented surface should fit the existing adapter pattern, but the
platform is newer and likely to require more careful handling than Gemini.

### Likely complexity

Moderate to moderately high.

Main reasons:
- newer platform surface
- more likely API churn
- less established release expectations for a comparative harness like this

### Benchmark value

Medium to high.

Grok would add public interest and comparative breadth, especially for
model-behavior comparison.

### Maintenance risk

Higher than Gemini.

Not because it is infeasible, but because it appears to be a newer integration
surface and may shift faster.

### Recommendation

**Viable, but second priority behind Gemini.**

Best treated as:
- next provider after Gemini
- or parallel evaluation work without immediate implementation commitment

## 3. Cohere

### Official API posture

Cohere has official documentation for:
- model catalog
- model listing
- chat endpoints

Sources:
- [Cohere models overview](https://docs.cohere.com/v2/docs/models)
- [Cohere list models](https://docs.cohere.com/reference/list-models)
- [Cohere chat endpoint](https://docs.cohere.com/reference/chat)

### SDK and request surface

The documented Python surface uses:
- `cohere.ClientV2()`
- `co.chat(...)`

This is clean enough for adapter work.

### Model discovery

Yes. Official model listing exists via:
- `GET /v1/models`

Source:
- [Cohere list models](https://docs.cohere.com/reference/list-models)

### Fit with current harness

Good.

Cohere’s chat-style interaction maps reasonably well onto the current harness
shape, especially for text-focused injection testing.

### Likely complexity

Moderate.

The adapter work should be comparable to the other providers already supported.

### Benchmark value

Medium.

Cohere is a credible provider and would improve breadth, but it may add less
headline value than Gemini for the next public step.

### Maintenance risk

Moderate.

The platform appears mature enough, but public attention and strategic value
for this specific release are probably lower than Gemini.

### Recommendation

**Strong third candidate.**

If the goal is to choose one “other AI model/provider” beyond Gemini and Grok,
Cohere is a defensible option.

## Comparative Recommendation

If only one provider is added next:

1. **Gemini**

If two providers are added next:

1. **Gemini**
2. **Grok**

If a third provider candidate needs to be documented for later expansion:

3. **Cohere**

After that:

4. **open-source / open-weight provider paths**

## Release Strategy Recommendation

For the current release cycle:

### Recommendation A — conservative

- finish current release hardening
- publish public technical preview with current providers
- implement Gemini next
- evaluate Grok and Cohere after release

### Recommendation B — controlled expansion

- finish current release hardening
- implement Gemini before public preview if schedule allows
- keep Grok and Cohere as documented next candidates

The more defensible choice is **Recommendation A** unless there is a strong
strategic reason to add Gemini immediately before release.

## 4. Open-Source / Open-Weight Options

### Why this class matters

After the hosted provider set expands, the next meaningful category is
open-source / open-weight model support.

This matters because it would let Invariant test:
- locally hosted models
- self-managed inference stacks
- OpenAI-compatible gateways for open-weight deployments
- enterprise-controlled model hosting paths

It also strengthens the project’s relevance beyond API-only evaluation.

### What this category includes

Likely candidates include:
- Llama-family deployments
- open-weight Mistral-family deployments
- other self-hosted or gateway-exposed inference stacks

The important point is that this is not one provider. It is a deployment class.

### Why it should not be the immediate next step

Open-weight support is strategically important, but it should come after the
next hosted-provider wave because:
- integration paths vary significantly
- local runtimes are less uniform than hosted APIs
- the test harness needs a clearer adapter policy for self-hosted endpoints

### Recommended integration posture

The likely cleanest path is:

1. support **OpenAI-compatible gateways** first
2. then evaluate whether direct runtime integrations are worth the additional
   complexity

This would allow Invariant to test a broad set of open-weight deployments
without committing immediately to every local runtime stack.

### What should be decided before implementation

Before building open-weight support, decide:
- whether Invariant should treat this as:
  - a provider category
  - or a transport/deployment mode
- whether support should begin with:
  - local-only targets
  - hosted inference endpoints
  - OpenAI-compatible gateways
- how model identity should be recorded for comparability across self-hosted
  systems

### Recommendation

Treat open-source / open-weight support as the **next provider class after
Cohere**, not as a one-off single provider.

This is the correct next expansion after the current hosted-provider sequence:

1. Gemini
2. Grok
3. Cohere
4. open-source / open-weight deployment paths

## Implementation Notes For Future Work

Each provider should be evaluated for:
- environment variable naming
- SDK dependency footprint
- adapter request mapping
- response normalization
- model listing support
- error handling
- live-test coverage
- UI model-picker integration

## Recommended Next Step

Do not implement immediately from this document alone.

First:
1. complete the current release hardening pass
2. decide whether the public technical preview should ship with the current
   provider set or include Gemini

Then:
3. implement the chosen next provider deliberately

After the hosted-provider wave:
4. define the open-weight integration strategy before implementation

## Related Documents

- [current_release_hardening_pass.md](/Users/jeffreysinason/Development/Invariant/docs/current_release_hardening_pass.md)
- [public_release_readiness.md](/Users/jeffreysinason/Development/Invariant/docs/public_release_readiness.md)
- [phased_build_plan.md](/Users/jeffreysinason/Development/Invariant/docs/phased_build_plan.md)
