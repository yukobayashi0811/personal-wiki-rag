# AI Agents Study Guide

**Summary**
This guide serves as a practical companion for the AI Agents course, helping learners understand the concepts, build a working agent demo, and connect the ideas into a cohesive system. It emphasizes building a small agent that helps a learner navigate the course material.

**Key Ideas**

*   **Agent vs. Chatbot:** An agent goes beyond a regular chatbot by being able to read/search course files, using tools, planning a learning path, maintaining context, remembering preferences, showing traces, and applying guardrails.
*   **Core Agent Components:** A complete agent system combines several parts:
    *   **Model:** The reasoning engine.
    *   **Tools:** Functions, APIs, or services the agent can use (e.g., searching the repository).
    *   **Knowledge:** Documents or data grounding the answer (e.g., lesson READMEs).
    *   **Context:** Information included in the current model call.
    *   **Memory:** Information saved for later use (e.g., preferred examples).
    *   **Planning:** Breaking a large goal into smaller steps.
    *   **Orchestration:** Routing work across tools, steps, or agents.
    *   **Trust:** Safety, security, evaluation, and observability.
*   **Learning Path:** Learners are encouraged to follow a single demo idea (e.g., a course helper agent) through the course lessons to see how each new capability adds to the agent's function.
*   **Practical Application (Course Helper Demo):** The goal is to build a small agent that, when asked how to learn about tool use, can:
    *   *Minimum Version:* Accept topic, find lessons, summarize, suggest task, show sources.
    *   *Stretch Version:* Remember preferences, use a plan, add self-check, log calls, ask for confirmation on high-impact actions.

**Source**
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

**Related Notes**
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
