# AI Agent Fundamentals

**Summary**
An Agent is a system that leverages an AI model to interact with its environment in order to achieve a user-defined objective. It functions as a loop: receiving a command, understanding natural language, engaging in reasoning and planning, executing actions using available tools, and observing the results to fulfill the task.

**Key Ideas**

*   **The Agentic Cycle:** An Agent operates by taking a command, interpreting it via natural language understanding, developing a plan (reasoning and planning), and executing that plan by interacting with its environment.
*   **Agent Architecture (Brain vs. Body):** An Agent is composed of two main parts:
    1.  **The Brain (AI Model):** The core thinking engine (often an LLM like GPT-4 or Llama) responsible for reasoning, planning, and deciding which actions to take.
    2.  **The Body (Capabilities and Tools):** The equipped capabilities that define the scope of possible actions. These are the external tools (e.g., a function to send an email) the Agent can use.
*   **Agency Spectrum:** Agents exist on a continuous spectrum defined by how much their output impacts the program flow, ranging from a simple processor (no impact) to a Multi-Agent system (one workflow triggering another).
*   **Actions vs. Tools:** An Action is the high-level goal (e.g., "Send Email"), while a Tool is the specific implementation (e.g., a Python function) that allows the Agent to execute that Action in the real world.

**Source**
[[raw/AI Agent Fundamentals.md|Source: AI Agent Fundamentals]]

**Related Notes**
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
