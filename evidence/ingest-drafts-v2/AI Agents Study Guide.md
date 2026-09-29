# AI Agents Study Guide

## Summary
This guide serves as a practical companion for the AI Agents course, helping users understand the concepts, build a small working agent demo, and connect the various components of an advanced agent system. It contrasts the capabilities of a sophisticated agent with those of a regular chatbot, emphasizing the roles of tools, planning, and memory.

## Key Ideas
*   **Agent vs. Chatbot:** An agent goes beyond a chatbot by being able to read/search course files, using tools (APIs, browsers), planning a learning path, maintaining context, remembering preferences, and showing traces/logs.
*   **Agent Components:** A complete agent system combines several parts:
    *   **Model:** The reasoning engine.
    *   **Tools:** Functions/APIs the agent can execute.
    *   **Knowledge:** Documents/data grounding the answer (e.g., course files).
    *   **Context:** Information included in the current model call.
    *   **Memory:** Information saved for later use.
    *   **Planning:** Breaking a large goal into smaller steps.
    *   **Orchestration:** Routing work across tools/steps/agents.
    *   **Trust:** Safety, security, evaluation, and observability.
*   **Learning Path:** The course recommends starting with Lessons 01-06 to build foundational vocabulary before specializing.
*   **Demo Project:** A suggested "course helper agent" demonstrates how to combine these concepts (e.g., finding lessons, summarizing, suggesting tasks).
*   **Production Readiness:** Deploying agents requires consideration of scalability, observability (tracking calls, latency, cost), and security (least-privilege tools, human approval).

## Source
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
