# Evaluating AI Agents

## Summary
Reliable evaluation is crucial for guiding model training and system improvement when building an Agent. Evaluation moves beyond simply building an Agent to scientifically grounding design choices (model choice, tool usage, knowledge base structure, etc.). A sound evaluation system must distinguish between "insufficient model capability" and "Harness design flaws." The evaluation process involves a complete system, not just the model, and requires a structured approach to ensure meaningful iteration.

## Key Ideas
*   **The Object of Evaluation:** The object being evaluated is the combination of the model and the Harness (the surrounding system components), not just the model itself.
*   **Distinguishing Bottlenecks:** To determine if the bottleneck is the model or the Harness, two experiments are key:
    *   **Model Swap:** Hold the Harness constant and swap the model. If a stronger model doesn't improve the score, the Harness is the bottleneck.
    *   **Ablation:** Disable one Harness component at a time to observe how overall performance changes.
*   **The Four Stages of Evaluation:** A complete evaluation system decomposes into four stages: defining success, sourcing tasks, identifying verifiers, and translating a score into a decision.
*   **Types of Metrics:**
    *   **Pass@k:** Run the same task $k$ times and count it as passed if at least one run passes (measures capability ceiling during exploration).
    *   **Pass$^k$:** Run the same task $k$ times consecutively, requiring every run to pass (measures reliability for production deployment).
*   **Repeatable Evaluation Environment:** A robust evaluation requires five components: Dataset (the task file), Environment State (mutable information), Tools (atomic operations for both Agent and user/environment), Rubric (checking layers), and Interaction Protocol (termination conditions).
*   **Environment Types (Verifiers):** Different tasks require different environments:
    *   *SingleTurnEnv:* No state/tools (e.g., math problems).
    *   *ToolEnv:* No state, multi-turn tool calls (e.g., search synthesis).
    *   *StatefulToolEnv:* State persistence, multi-turn tool calls (e.g., database modification).
    *   *SandboxEnv:* State persistence + isolation (e.g., code execution).

## Source
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
