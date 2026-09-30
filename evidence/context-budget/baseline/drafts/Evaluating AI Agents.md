# Evaluating AI Agents

## Summary
Reliable evaluation is crucial for guiding model training and system improvement when building Agent systems. Evaluation must move beyond simply testing the model to encompass the entire Agent system, including the "Harness" (prompts, tools, feedback loops). A sound evaluation system allows developers to distinguish between insufficient model capability and flaws in the Harness design.

## Key Ideas
*   **The Role of Evaluation:** Evaluation puts design choices (model choice, tool selection, knowledge base structure, memory implementation, etc.) on a scientific footing. Without a repeatable evaluation system, iteration is based on intuition.
*   **Systematic Testing:** Genuine capability gains are found through systematic comparative experiments (changing one variable) and ablation experiments (disabling one component).
*   **Harness vs. Model Bottleneck:** The object of evaluation is the combination of the model and the Harness. To determine if the bottleneck is the model or the Harness, a **model swap experiment** is recommended: hold the Harness constant and vary the model strength, observing the score change.
*   **Four Stages of Evaluation:** A complete evaluation system decomposes into four stages: what counts as success, where the tasks come from, who verifies, and how a score translates into a decision.
*   **Task Definition Components (Telecom Example):** A complex task requires several components:
    *   **Dataset:** The task file containing initial state, behavioral spec, and acceptance criteria.
    *   **Environment State:** The mutable information during execution (e.g., database records, device status).
    *   **Tools:** Atomic operations available to both the Agent and the user simulator.
    *   **Rubric:** The multi-layered checks (e.g., `env_assertions`, `actions`).
    *   **Interaction Protocol:** Specifies the order and termination conditions.
*   **Pass@k vs. Pass^k:**
    *   **Pass@k:** Run the task $k$ times and count it as passed if *at least one* run passes (measures capability ceiling during exploration).
    *   **Pass^k:** Run the task $k$ times in a row, requiring *every* run to pass (measures reliability for production deployment).

## Source
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
