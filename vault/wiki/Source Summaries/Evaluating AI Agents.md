---
reviewed: true
origin: legacy-v1
reviewed_on: 2026-09-29
review_basis: "evidence/ingest-drafts-context-budget/Evaluating AI Agents.md"
source: raw/Evaluating AI Agents.md
source_sha256: 813232a986ca3c16ba47d27c7f1d29903f7f1162df6456cba13ce899acbc3944
upstream_revision: d0daf079e7c8da56670886b48c329e9f9fc8281d
topic: Agent Evaluation
description: Tasks, metrics, verifiers, failure analysis, and production evaluation.
---

# Evaluating AI Agents

## Summary

Agent evaluation should measure the complete system—the model together with its harness—not the model in isolation. Prompts, tools, knowledge, memory, constraints, and feedback loops can change performance even when the underlying model remains fixed. A repeatable evaluation system turns design decisions into controlled experiments and provides evidence for improvement.

## Model Versus Harness Bottlenecks

Two experiments help locate the cause of poor performance:

- **Ablation:** disable one harness component and observe how the overall result changes. This identifies which internal component matters.
- **Model swap:** hold the harness constant and replace only the model. If a stronger model does not improve the score, the harness is probably the bottleneck; large changes across models suggest that model capability is limiting performance.

These methods answer different questions and should not be treated as interchangeable.

## Four Stages of Evaluation

A complete evaluation system establishes:

1. what counts as success;
2. where representative tasks come from;
3. who or what verifies the outcome;
4. how scores translate into engineering or product decisions.

Evaluation tasks should specify the initial state, the user request, the expected outcome, and the rules used by a verifier. The environment must expose the same tools and state transitions that the real agent encounters.

## Capability and Reliability Metrics

- **Pass@k** succeeds when at least one of *k* attempts passes. It is useful for estimating a capability ceiling during exploration.
- **Pass^k** succeeds only when all *k* attempts pass. It emphasizes consistency and is more relevant to production reliability.

A single successful run can therefore demonstrate possibility without demonstrating dependable behavior.

## Evaluation Environments and Verification

Different tasks require different environments, ranging from single-turn tasks without tools to stateful, isolated environments for multi-step execution. Verification may use deterministic checks, human review, model-based judges, or combinations of these methods. Strong evaluation also examines trajectories so that the first incorrect decision can be distinguished from later consequences.

For open-ended tasks, an LLM-as-a-Judge should apply a self-contained rubric covering factual accuracy, coherence, completeness, safety, and explicit pitfalls. Criteria can be weighted as essential, important, optional, or veto items; a hallucination veto, for example, can invalidate an otherwise strong response. Judge design must also account for biases such as preferring longer answers, so heterogeneous judges or pairwise comparisons are safer than treating one score as objective truth.

## Failure Attribution and Regression Tasks

A failed end-to-end score becomes actionable only after locating the first unacceptable step, recording the error class, identifying the responsible model output or tool call, and preserving auditable evidence. Later mistakes may be consequences rather than the root cause.

Once the first error is known, it can become one of two regression forms:

- **End-to-end regression:** rerun the complete task from its initial state and verify the final outcome and safety conditions.
- **Trajectory-prefix regression:** freeze the context, conversation, tool results, and environment immediately before the first error, then evaluate only the next observable action or small set of actions.

Trajectory-prefix cases are cheaper and isolate a single decision boundary, while end-to-end cases verify that the complete workflow still succeeds.

## Cost Analysis

Agent cost is not just the listed per-token price. Repeated model calls resend accumulated conversation and tool output, thinking-capable models may consume hidden thinking tokens, and external tools and infrastructure add direct and indirect costs. Stable-prefix cache reuse, context compression, tiered model routing, and task-level cost caps should therefore be evaluated on complete workflows. Savings from separate optimizations should be measured together rather than added arithmetically.

## Observability and Improvement

Useful traces include model inputs and outputs, tool calls, observations, state changes, latency, resource use, and failure categories. Results should lead to hypotheses and controlled changes rather than unstructured prompt editing. Statistical analysis, regression tests, feature flags, A/B tests, and privacy-aware analytics help convert evaluation from a one-time benchmark into production infrastructure.

## Source

- [[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]
- Original: *Understanding AI Agent: Design Principles and Engineering Practices*, Chapter 7, “Evaluating Agents”

## Related Notes

- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]] — supplies the basic model, tool, action, and agency concepts being evaluated.
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]] — places evaluation alongside RAG, context, memory, planning, observability, and security.
- [[wiki/Concepts/Model Swap Experiment|Model Swap Experiment]] — isolates the controlled comparison used to diagnose model versus harness limitations.
