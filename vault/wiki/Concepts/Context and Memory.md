---
reviewed: true
origin: curated
topic: Agent System Design
description: The boundary between current-call context and information retained for later.
---

# Context and Memory

## Core Distinction

Context is the information the model sees in the current call. Too little context can omit important details, while too much can increase latency, cost, or confusion.

Memory is information saved for later interactions. The study guide recommends saving only information that is useful, safe, and easy to update or delete.

## Design Implication

Context engineering selects information for the next model call; memory design decides what should remain available beyond that call.

## Related Notes

- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]] — provides the source definitions and practical guidance summarized here.
- [[wiki/Concepts/Tools and Actions|Tools and Actions]] — shows another boundary between model-visible information and capabilities supplied by the harness.

## Sources

- [[raw/AI Agents Study Guide.md#Context|AI Agents Study Guide — Context]]
- [[raw/AI Agents Study Guide.md#Memory|AI Agents Study Guide — Memory]]
