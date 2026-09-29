---
reviewed: false
origin: legacy-v1
ingest_protected: true
source: raw/AI Agent Fundamentals.md
source_sha256: 7b40365e7f037ae8dbc6d94fb570ff92a43d038a489824b91e06105d2a17e3d7
upstream_revision: b3946b1d09d29c65736e219d48a8a736a2c52154
topic: Agent Foundations
description: Definitions, agency levels, reasoning, planning, tools, and actions.
---

# AI Agent Fundamentals

## Summary

An AI agent uses a model to pursue a user-defined objective by reasoning, planning, and interacting with an environment. The model decides what should happen next, while the surrounding system gives it concrete capabilities through tools. This combination lets an agent move beyond producing text and take actions that affect program flow or the outside world.

## Core Definition

The source defines an agent as a system that leverages an AI model to interact with its environment in order to achieve a user-defined objective. Three capabilities are central:

1. **Reasoning:** interpreting the request and the current situation.
2. **Planning:** deciding which steps and resources are needed.
3. **Acting:** using available tools and incorporating the resulting observations.

The model is the agent's “brain.” It handles reasoning, planning, and action selection. Tools and other capabilities form the “body,” determining what actions the agent can actually perform.

## Agency as a Spectrum

Agency is not an all-or-nothing property. Systems can grant a model progressively more control:

- A simple processor produces output without changing program flow.
- A router selects between predefined paths.
- A tool caller chooses a function and its arguments.
- A multi-step agent controls an iterative process.
- A multi-agent system can initiate other agentic workflows.

This spectrum is useful because an application should receive only the degree of autonomy needed for its task.

## Tools and Actions

Language models normally produce text. Developers give an agent practical capabilities by implementing tools such as search, messaging, image generation, or database access. A tool is a callable capability; an action is the task-level step the agent performs, which may involve one or more tools. Tool design therefore limits both the usefulness and the risk of the resulting agent.

## Common Applications

The source describes personal assistants, customer-service systems, and game characters as examples. In each case, the model interprets natural-language input while tools connect it to data or actions in an environment.

## Source

- [[raw/AI Agent Fundamentals.md|Source: AI Agent Fundamentals]]
- Original: Hugging Face Agents Course, “What is an Agent?”

## Related Notes

- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]] — expands the architecture with knowledge, context, memory, orchestration, RAG, and trust.
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]] — explains how to measure the combined model-and-harness system.
- [[wiki/Concepts/Tools and Actions|Tools and Actions]] — develops the source's distinction between a tool and an action.
