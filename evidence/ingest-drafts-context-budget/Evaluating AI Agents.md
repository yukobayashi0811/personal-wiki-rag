# Evaluating AI Agents

**Summary**
Evaluating AI Agents is a complex, multi-stage process that moves beyond simply scoring an outcome. A robust evaluation system requires defining success, sourcing tasks, selecting a verification method, and translating scores into actionable decisions. The process involves building a closed loop where failure attribution and continuous data collection (observability) drive iterative improvements to the Agent's Harness, model, or knowledge base. The shift from public benchmarks to production deployment requires moving from deterministic checks to probabilistic judgment.

**Key Ideas**

*   **The Role of the Harness:** The object of evaluation is not just the model, but the combination of the model and its surrounding system (the Harness: prompts, tools, knowledge base, feedback loops). A poor performance score may indicate a flaw in the Harness design, not the model itself.
*   **Verification Techniques:**
    *   **Ablation Experiments:** Disable one component of the Harness to observe performance change.
    *   **Model Swap Experiments:** Hold the Harness constant and swap the model to isolate whether the bottleneck is the model or the Harness.
    *   **Regression Tasks:**
        *   *End-to-end:* Tests the entire workflow from initial state to final outcome.
        *   *Trajectory-prefix:* Freezes the context just before a decision point, testing only the next observable action (cheaper, isolates specific policy/tool problems).
*   **Advanced Evaluation Components:**
    *   **Rubric (Scoring Criteria):** Breaks vague success into multiple scorable dimensions (e.g., Factual Correctness, Completeness, Reasoning). It must include a **Veto mechanism** (e.g., hallucination) and be grounded in domain knowledge.
    *   **LLM-as-a-Judge:** Used when tasks are open-ended. Requires guarding against biases like **Length Bias** by using multi-source, heterogeneous judging and pairing comparisons.
    *   **Cost Analysis:** Must account for non-linear costs: **Context Accumulation Effect** (growing cost with each round due to sending full history) and **Thinking Token Cost**.
*   **Data-Driven Iteration:**
    *   **Observability:** Traces (LLM calls, tool calls, retrievals) are essential for diagnosis, identifying bottlenecks, and turning failure cases into future regression tests.
    *   **Pass@k vs. Pass^k:** *Pass@k* measures the ceiling of capability (at least one run succeeds), while *Pass^k* measures business reliability (k consecutive runs succeed).
    *   **Failure Attribution:** Pinpointing the exact step where the task went off course (e.g., "wrong information reported to the user" vs. "model cannot do OCR") is crucial for targeted fixes.

**Source**
[[raw/Evaluating AI Agents.md|Source: Evaluating AI Agents]]

**Related Notes**
- [[wiki/Source Summaries/AI Agent Fundamentals|AI Agent Fundamentals]]
- [[wiki/Source Summaries/AI Agents Study Guide|AI Agents Study Guide]]
