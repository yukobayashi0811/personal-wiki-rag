# AI Agents Study Guide

## Summary
This guide serves as a practical companion for the AI Agents course, helping learners understand the concepts, build a working agent demo, and connect the theoretical parts of agent systems (Model, Tools, Knowledge, Context, Memory, Planning, Orchestration, Trust) to practical implementation. It outlines a structured approach to learning, starting with foundational lessons and building up to advanced production concepts.

## Key Ideas
*   **Agent vs. Chatbot:** An agent goes beyond a regular chatbot by being able to read/search course files, using tools, planning a learning path, maintaining context, remembering preferences, and showing traces/logs.
*   **Agent Components:** A complete agent system combines several parts:
    *   **Model:** The reasoning engine.
    *   **Tools:** Functions, APIs, or services the agent can use (e.g., `search_lessons(query)`).
    *   **Knowledge:** Documents grounding the answer (e.g., lesson READMEs).
    *   **Context:** Information included in the current model call.
    *   **Memory:** Information saved for later use (e.g., preferred examples).
    *   **Planning:** Breaking a large goal into smaller steps.
    *   **Orchestration:** Routing work across tools and steps.
    *   **Trust:** Safety, security, evaluation, and observability (logging, guardrails).
*   **Learning Path:** New learners should complete Lessons 01-06 first. A suggested "course helper agent" demo provides a running example through the course.
*   **Production Considerations:** Deploying agents requires considering scalability, observability (tracking calls, latency, cost), and security (least-privilege tools, human approval).

## Source
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
