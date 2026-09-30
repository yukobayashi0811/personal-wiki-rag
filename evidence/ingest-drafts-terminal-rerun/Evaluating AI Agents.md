# Evaluating AI Agents

## Summary
Reliable evaluation is crucial for guiding model training and system improvement when building Agent systems. Evaluation moves beyond simply building an Agent to rigorously testing the entire system—the combination of the model and its Harness. A sound evaluation system must distinguish between insufficient model capability and flaws in the Harness design.

## Key Ideas
*   **The Role of Evaluation:** Evaluation puts design choices (model choice, tool usage, knowledge base structure, prompt organization, constraints) on a scientific footing. It prevents intuition-based iteration and allows for genuine capability gains to be distinguished from superficial fluctuations.
*   **Systematic Testing:** To improve an Agent, one must use systematic comparative experiments (changing one variable at a time) and ablation experiments (disabling one component at a time).
*   **Model vs. Harness:** When an Agent performs poorly, the fix might be a better Harness component (prompts, tool design) rather than a different model. A "model swap experiment" (holding the Harness constant and changing the model) is key to determining if the bottleneck is the model or the Harness.
*   **The Four Stages of Evaluation:** A complete evaluation system decomposes into four stages: what counts as success, where the tasks come from, who verifies, and how a score translates into a decision.
*   **Pass@k vs. Pass^k:**
    *   **Pass@k:** Run the task $k$ times and count it as passed if at least one run passes (measures capability ceiling during exploration).
    *   **Pass^k:** Run the task $k$ times consecutively, requiring every run to pass (measures reliability for production deployment).
*   **Repeatable Evaluation Environment:** A robust evaluation requires five components: Dataset (the task file), Environment State (mutable information, must be resettable), Tools (atomic operations for both Agent and user/environment), Rubric (scoring layers), and Interaction Protocol (order and termination conditions).
*   **Verifier Frameworks:** Environments can be classified by their needs: `SingleTurnEnv` (no state/tools), `ToolEnv` (no state, multi-turn tools), `StatefulToolEnv` (stateful, multi-turn tools), and `SandboxEnv` (stateful + isolated execution).

## Source
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
