# Evaluating AI Agents

## Summary
Reliable evaluation is critical for guiding model training and system improvement when building Agent systems. Evaluation moves beyond simply building an Agent to scientifically grounding design choices (model choice, tool usage, knowledge structure, etc.). A sound evaluation system must distinguish between insufficient model capability and flaws in the surrounding Harness design.

## Key Ideas

*   **The Role of Evaluation:** Evaluation provides a scientific footing to address complex design choices inherent in Agent construction. Without a repeatable evaluation system, an Agent is only iterated on intuition.
*   **Distinguishing Bottlenecks:** To determine if a poor performance is due to the model or the Harness, a **model swap experiment** is recommended: hold the Harness constant and vary the model strength, observing the score change.
*   **Components of a Complete Evaluation System:** A full evaluation system decomposes into four stages: defining success, sourcing tasks, defining verifiers, and mapping scores to decisions.
*   **The Telecom Task Example ($\tau^2$-bench):** A detailed example of a complex task involves five components: Dataset (the task file), Environment State (mutable information), Tools (operations for both Agent and user), Rubric (checking layers), and Interaction Protocol (order/termination).
*   **Types of Environments (Verifiers):** Different tasks require different environments:
    *   `SingleTurnEnv`: No state persistence, no tool calls (e.g., math problems).
    *   `ToolEnv`: No state persistence, multi-turn tool calls (e.g., search/synthesis).
    *   `StatefulToolEnv`: State persistence, multi-turn tool calls (e.g., database modification).
    *   `SandboxEnv`: State persistence + isolation (e.g., code execution).
*   **Success Metrics:**
    *   **Pass@k:** Run the same task $k$ times; pass if at least one run succeeds (measures capability ceiling/exploration).
    *   **Pass$^k$:** Run the same task $k$ times consecutively; pass only if all runs succeed (measures reliability/production readiness).

## Source
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

## Related Notes
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
