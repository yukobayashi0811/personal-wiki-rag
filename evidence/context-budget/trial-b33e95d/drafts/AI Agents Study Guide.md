# AI Agents Study Guide

## Summary
This guide serves as a practical companion for the AI Agents course, designed to help users navigate the lessons, understand the core concepts, and build a working agent demonstration. The recommended approach is to follow a single demo idea (like a "course helper agent") through the lessons, seeing how each new capability adds to the agent's functionality.

## Key Ideas

### Agent vs. Chatbot
A sophisticated agent goes beyond a regular chatbot by possessing advanced capabilities, including:
*   Reading or searching course files.
*   Using external tools (APIs, browsers, services).
*   Planning multi-step learning paths.
*   Maintaining context from the conversation.
*   Remembering useful preferences (memory).
*   Showing traces, citations, or logs (observability).
*   Applying guardrails before risky actions.

### Core Agent Components
A complete agent system combines several parts:

| Part | Plain-language meaning | Function in Demo |
| :--- | :--- | :--- |
| **Model** | The reasoning engine | Interprets the user's request. |
| **Tools** | Functions, APIs, services the agent can use | Searches the repository or retrieves lesson content. |
| **Knowledge** | Documents used to ground the answer | Course README files and lesson material. |
| **Context** | Information included in the next model call | The user's goal and the tool results. |
| **Memory** | Information saved for later use | Learner preferences (e.g., Python examples). |
| **Planning** | Breaking a larger goal into smaller steps | Finding lessons, summarizing them, suggesting a task. |
| **Orchestration** | Routing work across tools, steps, or agents | A planner calls a search tool, then a summarizer. |
| **Trust** | Safety, security, evaluation, and observability | Logs tool calls and asks before high-impact actions. |

### Concepts Explained
*   **Tool:** An external function with a clear name, narrow job, typed inputs, and predictable output (e.g., `search_lessons(query)`).
*   **RAG (Retrieval-Augmented Generation):** Grounding the agent's answer in specific source material (e.g., lesson READMEs, code samples).
*   **Planning:** Necessary when a request requires multiple steps (e.g., Find lessons $\rightarrow$ Summarize $\rightarrow$ Suggest task).
*   **Context:** The information the model sees *right now* for the current call.
*   **Memory:** Information saved across interactions that is useful and safe to retain.
*   **Evaluation vs. Observability:** Evaluation asks if the agent did the right thing; Observability asks how the agent arrived at its answer (logs, traces).

### Learning Path
*   **Beginners:** Do not skip Lessons 01-06, as they provide the necessary vocabulary.
*   **Advanced:** The course is structured to allow jumping into specific paths based on goals (e.g., building a RAG agent starts with Lesson 05).
*   **Production:** The Microsoft Agent Framework (MAF) and Azure OpenAI Responses API are the recommended paths for production deployment.

## Source
[[raw/AI Agents Study Guide.md|Source: AI Agents Study Guide]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
