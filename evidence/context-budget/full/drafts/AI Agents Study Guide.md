# AI Agents Study Guide

## Summary
This guide serves as a practical companion for the AI Agents course, helping learners understand how to apply concepts, build a small working agent demo, and connect the various components of an agent system. It emphasizes moving beyond a simple chatbot by building an agent capable of planning, using tools, and maintaining context to achieve complex goals.

## Key Ideas
*   **Agent vs. Chatbot:** A sophisticated agent surpasses a regular chatbot by possessing advanced capabilities, including reading/searching course files, using external tools (APIs, functions), planning multi-step learning paths, maintaining conversation context, and providing execution traces/logs.
*   **Agent System Architecture:** A complete agent system integrates several core components:
    *   **Model:** The reasoning engine interpreting requests.
    *   **Tools:** Functions or services the agent can execute (e.g., search, retrieve lesson content).
    *   **Knowledge:** Grounding data (e.g., course READMEs, lesson material).
    *   **Context:** Information included in the current model call.
    *   **Memory:** Information saved for later use across interactions.
    *   **Planning/Orchestration:** Breaking down large goals into smaller, executable steps and routing work across tools.
    *   **Trust:** Safety, security, evaluation, and observability (logging tool calls, applying guardrails).
*   **Learning Approach:** Beginners should complete Lessons 01-06 first to establish the necessary vocabulary. A practical approach is to follow one demo idea (like a "course helper agent") through the course, asking how each new lesson adds capability.
*   **Production Readiness:** The recommended technical stack uses the Microsoft Agent Framework (MAF) targeting the Azure OpenAI Responses API. Production deployment requires considerations like smoke testing, observability (tracking latency, cost, failures), and security (least-privilege tools, human approval).

## Source
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
