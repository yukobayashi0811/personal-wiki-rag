# Evaluating AI Agents

## Summary
Reliable evaluation is crucial for guiding model training and system improvement when building Agent systems. Evaluation moves beyond simply testing the model; it involves a scientific process of comparing the model's performance against the entire system (the model combined with its Harness). A sound evaluation system must be able to distinguish between insufficient model capability and flaws in the Harness design.

## Key Ideas

*   **The Role of Evaluation:** Evaluation puts design choices (model choice, tool selection, knowledge base structure, prompt organization, constraints, etc.) on a scientific footing. Without a repeatable evaluation system, an Agent is only iterated upon intuition.
*   **Systematic Testing:** To gain genuine insights, developers must use systematic comparative experiments (changing one variable) and ablation experiments (disabling one component).
*   **Model vs. Harness Bottleneck:** When an Agent performs poorly, the fix might be a better Harness component, not a different model. The **model swap experiment** (holding the Harness constant and changing the model) is a key method to determine if the bottleneck is the model or the Harness.
*   **The Four Stages of Evaluation:** A complete evaluation system decomposes into four stages: defining what counts as success, where the tasks originate, who verifies the outcome, and how a score translates into a decision.
*   **Pass@k vs. Pass^k:**
    *   **Pass@k:** Run the task $k$ times and count it as passed if at least one run succeeds (measures capability ceiling during exploration).
    *   **Pass^k:** Run the same task $k$ times in a row, requiring every run to pass (measures reliability needed for production deployment).
*   **Components of a Repeatable Evaluation Environment:** A robust evaluation environment requires five components:
    1.  **Dataset:** The task file containing initial state, behavioral spec, and acceptance criteria.
    2.  **Environment State:** The mutable information (e.g., database contents, device status) that must be resettable.
    3.  **Tools:** Atomic operations available to both the Agent and the user/environment.
    4.  **Rubric:** The multi-layered checks (e.g., `env_assertions`, `actions`) and the aggregation rule (`reward_basis`).
    5.  **Interaction Protocol:** Specifies the order of interaction and termination conditions.
*   **Verifier Types:** Evaluation environments can be classified by their requirements:
    *   `SingleTurnEnv`: No state persistence, no tool calls (e.g., math problems).
    *   `ToolEnv`: No state persistence, multi-turn tool calls (e.g., search/synthesis).
    *   `StatefulToolEnv`: State persistence, multi-turn tool calls (e.g., database modification).
    *   `SandboxEnv`: State persistence + isolation (e.g., code execution).

## Source
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
