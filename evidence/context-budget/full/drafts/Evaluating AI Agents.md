# Evaluating AI Agents

**Summary**
Evaluating AI Agents is a complex, multi-stage process that moves beyond simple pass/fail scoring to provide actionable insights for continuous system improvement. A robust evaluation system must account for the interaction between the model and its surrounding "Harness" (prompts, tools, memory, etc.). The process involves designing a high-fidelity evaluation environment, creating a specific dataset, applying rigorous verification methods, and, crucially, translating performance scores into concrete hypotheses for improvement. The most advanced systems embed this evaluation into the product itself, making it a continuous, data-driven engineering cycle.

**Key Ideas**

*   **The Holistic View (Model + Harness):** When an Agent performs poorly, the bottleneck may not be the model itself, but the Harness (e.g., poor prompt design, flawed tool integration). A "model swap experiment" (holding the Harness constant and changing the model) is essential to isolate whether the issue is model capability or Harness design.
*   **High-Fidelity Evaluation Environments:** A complete evaluation system decomposes into four stages: defining success, sourcing tasks, defining the verifier, and mapping scores to decisions. High-fidelity environments (like $\tau^2$-bench) use components like a user simulator, a business database, and a multi-layered rubric to model real-world constraints, including progressive information disclosure and dual control (where both Agent and user can affect the environment).
*   **Metrics and Reliability:** It is critical to distinguish between:
    *   **Pass@k:** The capability ceiling (at least one run succeeds out of $k$).
    *   **Pass$^k$:** The business reliability (all $k$ consecutive runs succeed).
    *   **Cost/Latency:** Throughput (Prefill/Decode speed) and Latency (TTFT/p95 tail latency) must be analyzed together with cost to determine the true cost-performance ratio.
*   **Advanced Verification and Attribution:** For production systems, verification must move beyond deterministic checks.
    *   **LLM-as-a-Judge:** Uses a language model to score outputs against a detailed **Rubric** (Scoring Criteria) that includes Essential, Important, Optional, and Veto items (e.g., hallucination).
    *   **Failure Attribution:** For continuous improvement, every failure must be traced back to a primary error class (e.g., "Requirement understanding," "Tool-call error") and the specific step where the error began, allowing for targeted fixes.
    *   **Regression Tasks:** **End-to-end** tasks check final state; **Trajectory-prefix** tasks freeze the context just before an error to isolate a single decision boundary, making them ideal for high-reliability production Agents.

**Source**
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

**Related Notes**
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
<|channel>
