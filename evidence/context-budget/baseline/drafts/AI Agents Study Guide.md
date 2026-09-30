# AI Agents Study Guide

## Summary
This guide serves as a practical companion for the AI Agents course, helping users understand the concepts, build a working agent demo, and connect theoretical lessons to practical application. It emphasizes building a small agent (like a "course helper agent") throughout the course to apply concepts like planning, tool use, and memory.

## Key Ideas
*   **Agent vs. Chatbot:** An agent goes beyond a regular chatbot by being able to read/search course files, using tools, planning a learning path, maintaining context, remembering preferences, and showing traces/logs.
*   **Core Agent Components:** A complete agent system combines several parts:
    *   **Model:** The reasoning engine.
    *   **Tools:** Functions, APIs, or services the agent can use (e.g., searching the repository).
    *   **Knowledge:** Documents or data used to ground the answer (e.g., lesson READMEs).
    *   **Context:** Information included in the current model call.
    *   **Memory:** Information saved for later use (e.g., user preferences).
    *   **Planning:** Breaking a large goal into smaller steps.
    *   **Orchestration:** Routing work across tools, steps, or agents.
    *   **Trust:** Safety, security, evaluation, and observability (e.g., logging tool calls).
*   **Learning Path:** The course is structured to be followed sequentially (Lessons 01-06 are crucial for vocabulary) or by goal (e.g., building a RAG agent, understanding multi-agent systems).
*   **Practical Application:** The ideal project is a "course helper agent" that accepts a topic, finds relevant lessons, summarizes them, and suggests a practice task.
*   **Production Readiness:** For production deployment, the Microsoft Agent Framework (MAF) and Azure OpenAI Responses API are recommended, requiring consideration of latency, cost, and failure modes.

## Source
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
