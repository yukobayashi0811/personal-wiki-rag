# Fixed Evaluation Set

This answer key is intentionally stored outside `vault/` so it cannot be retrieved as wiki evidence. The four questions were fixed before final answer generation.

## Q1 — Agent Anatomy

**Question:** What are the two main parts of an AI agent?

**Expected evidence:** `AI Agent Fundamentals.md`, in the sections that describe the model as the agent's brain and its capabilities and tools as the body.

**Pass condition:** The answer identifies the AI model and the available tools or capabilities, explains their respective roles, and cites the supplied passages.

## Q2 — Context and Memory

**Question:** How are context and memory defined in an agent system?

**Expected evidence:** `AI Agents Study Guide.md`, where context is information included in the next model call and memory is information saved for later use.

**Pass condition:** The answer clearly distinguishes information available to the current or next model call from information retained for future interactions, with citations.

## Q3 — Model Versus Harness Bottleneck

**Question:** How can a team distinguish a model capability bottleneck from a harness design bottleneck?

**Expected evidence:** `Evaluating AI Agents.md`, especially the model-swap experiment and the discussion of ablation.

**Pass condition:** The answer holds the harness constant while changing the model, interprets small versus large score changes correctly, and may distinguish that experiment from component ablation. Every factual claim must be cited.

## Q4 — Unsupported Market Data

**Question:** What was the global revenue of the AI agent market in 2024?

**Expected evidence:** None of the three sources contains a supported market-revenue figure.

**Pass condition:** The system returns exactly: `The available sources do not contain enough evidence to answer this question.` It must not guess or use model memory.
