# Evaluating AI Agents

**Summary**
Evaluating AI Agents is a continuous, multi-stage engineering process that moves beyond simple outcome scoring. It requires building a comprehensive system—including a defined task, a controlled environment, and a rigorous verification mechanism—to diagnose the root cause of failure. The goal is not merely to measure performance but to identify whether the issue lies with the model's capability, the surrounding "Harness" (prompts, tools, feedback loops), or the evaluation system itself. Advanced production systems embed this evaluation into a closed loop of continuous iteration.

**Key Ideas**

*   **The Holistic View (Harness):** The object of evaluation is the combination of the model and its Harness. A poor score may indicate a Harness design flaw (e.g., prompt organization, tool design) rather than an insufficient model.
*   **Diagnostic Techniques:**
    *   **Model Swap:** Holds the Harness constant and changes the model to determine if the model is the bottleneck.
    *   **Ablation:** Holds the model constant and disables a Harness component to observe how overall performance changes.
*   **Advanced Task Design ($\tau^2$-bench):** High-fidelity benchmarks often employ:
    *   **Progressive Information Disclosure:** The environment only reveals information as the Agent prompts for it.
    *   **Dual-Control Environment:** Both the Agent and the simulated user/environment possess independent tools and control over the state.
    *   **Layered Verification:** Success is checked across multiple dimensions (e.g., actions taken, final state, communication).
*   **Scaling Success Metrics:**
    *   **Pass@k:** Measures the ceiling on capability (at least one run passes out of $k$).
    *   **Pass^k:** Measures business reliability (requiring $k$ consecutive runs to pass).
*   **LLM-as-a-Judge and Rubrics:** For open-ended tasks, a Rubric guides the LLM judge. A robust Rubric must include:
    *   **Veto Mechanism:** A critical error (e.g., hallucination) that automatically invalidates the entire response.
    *   **Standardized Weighting:** Classifying criteria as Essential, Important, or Optional.
    *   **Self-Contained Evaluation:** Criteria must be objectively verifiable and independent of the evaluator's domain knowledge.
*   **Production Reality & Cost:**
    *   **Observability:** Tracing execution paths (LLM calls, tool calls, retrieval) is crucial for diagnosis and continuous optimization.
    *   **Cost Complexity:** True cost includes not just token price, but the **Context Accumulation Effect** (growing cost from resending history) and **Thinking Token Cost** (billed for internal reasoning).
    *   **Regression Tasks:** Failure attribution allows converting production errors into repeatable **trajectory-prefix regression tasks** (testing the next few actions) or **end-to-end regression tasks** (testing the full workflow).

**Source**
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

**Related Notes**
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
