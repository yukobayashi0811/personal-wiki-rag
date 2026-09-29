# AI Agent Fundamentals

**Summary**
An Agent is a system that leverages an AI model to interact with its environment to achieve a user-defined objective. It combines reasoning, planning, and the execution of actions (often via external tools) to fulfill tasks.

**Key Ideas**

*   **Definition:** An Agent is an AI model capable of reasoning, planning, and interacting with its environment. The ability to interact with the environment is referred to as its "agency."
*   **The Agent Process:** An Agent follows a cycle to achieve a goal:
    1.  **Receives Command:** Interprets natural language instructions.
    2.  **Reasoning and Planning:** Analyzes the situation and devises a plan, determining necessary steps and tools.
    3.  **Action:** Executes the plan by utilizing available tools.
    4.  **Interaction:** Brings the outcome back to the environment.
*   **Agent Components:**
    *   **The Brain (AI Model):** Handles the thinking—reasoning, planning, and deciding which Actions to take.
    *   **The Body (Capabilities and Tools):** Represents the physical or digital capabilities the Agent possesses (e.g., a coffee machine, a coding environment).
*   **LLMs and Tools:** The most common AI model is the LLM (e.g., GPT-4, Llama), which takes and outputs text. To perform actions beyond text generation (like creating an image or sending an email), the LLM must utilize external **Tools**.
*   **Actions vs. Tools:** An **Action** is the high-level task performed by the Agent, while a **Tool** is a specific external function (like a Python function) that the Agent uses to execute an Action.

**Source**
[[raw/AI Agent Fundamentals.md|Source: AI Agent Fundamentals]]

**Related Notes**
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]]
