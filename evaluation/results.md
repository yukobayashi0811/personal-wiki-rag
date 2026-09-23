# Evaluation Results

Evaluation date: 2026-09-22 PDT (2026-09-23 UTC)

All final model-backed checks used `mlx-community/gemma-4-e4b-it-4bit` through MLX-LM 0.31.3. The model and all evidence were local. The final set below ran inside one operating-system network-denied session. The fixed questions and pass conditions are defined in [`questions.md`](questions.md), and the full offline demonstration is indexed in [`evidence/offline-demo/README.md`](../evidence/offline-demo/README.md).

## Fixed Ask Questions

| Question | Result | Evidence | Assessment |
| --- | --- | --- | --- |
| Q1: Agent anatomy | Pass | [`20260923T051741822234Z-ask.md`](../evidence/offline-demo/runs/20260923T051741822234Z-ask.md) | Identified the model as the brain and capabilities/tools as the body. All material claims cite S1. |
| Q2: Context and memory | Pass | [`20260923T051756564232Z-ask.md`](../evidence/offline-demo/runs/20260923T051756564232Z-ask.md) | Correctly defined current-call context and saved-for-later memory. Both definitions cite S5, the relevant study-guide passage. |
| Q3: Model versus harness bottleneck | Pass after one previously diagnosed generation failure | [`20260923T051814816080Z-ask.md`](../evidence/offline-demo/runs/20260923T051814816080Z-ask.md) | Correctly described a controlled model swap, interpreted small versus large score changes, and distinguished model swapping from ablation. |
| Q4: Unsupported market revenue | Pass | [`20260923T051818429817Z-ask.md`](../evidence/offline-demo/runs/20260923T051818429817Z-ask.md) | Returned the exact insufficient-evidence response instead of guessing. |

The first Q3 attempt ended mid-sentence after using the original 700-token generation budget. The failed record is retained at [`20260923T043130284355Z-ask.md`](../evidence/runs/20260923T043130284355Z-ask.md). Retrieval had selected the correct passage, so the fault was isolated to generation. Increasing the default budget to 1,400 tokens produced the complete passing answer above.

## Mode-Boundary Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Capability question does not trigger retrieval | Pass; zero passages retrieved | [`20260923T051828138943Z-chat.md`](../evidence/offline-demo/runs/20260923T051828138943Z-chat.md) |
| Drafting request does not trigger retrieval | Pass; zero passages retrieved | [`20260923T051841680188Z-chat.md`](../evidence/offline-demo/runs/20260923T051841680188Z-chat.md) |
| Follow-up uses chat history | Pass; “Make that shorter” condensed the immediately preceding plan with zero retrieval | [`20260923T051849524126Z-chat.md`](../evidence/offline-demo/runs/20260923T051849524126Z-chat.md) |
| Explicit note request triggers retrieval and citations | Pass; five passages retrieved and factual claims cite S1 | [`20260923T051910680828Z-chat.md`](../evidence/offline-demo/runs/20260923T051910680828Z-chat.md) |
| Search returns raw text and source locations without generation | Pass; model is recorded as not used | [`20260923T051910879741Z-search.md`](../evidence/offline-demo/runs/20260923T051910879741Z-search.md) |
| Ask cannot use a fact introduced only in chat | Pass; chat retained “teal,” while a separate ask returned insufficient evidence | [`20260923T051917440812Z-chat.md`](../evidence/offline-demo/runs/20260923T051917440812Z-chat.md), [`20260923T051920330081Z-chat.md`](../evidence/offline-demo/runs/20260923T051920330081Z-chat.md), [`20260923T051924078743Z-ask.md`](../evidence/offline-demo/runs/20260923T051924078743Z-ask.md) |

## Performance Measurements

- Fresh model-backed ingestion of three sources produced 176 passages and three wiki-note drafts in 95.26 seconds with a maximum resident set size of 5,399,969,792 bytes (approximately 5.40 GB). The operating-system sandbox denied network access for the entire run.
- The final offline Q1 answer completed in 10.89 seconds and ended at 4.700 GB process resident memory.
- The longest passing final fixed answer, Q3, completed in 16.29 seconds and ended at 4.701 GB process resident memory.
- Indexing without note generation remains separately measured in [`ingestion-benchmark.md`](../evidence/setup/ingestion-benchmark.md) so retrieval cost is distinguishable from generation cost.

## Observed Limitation and Improvement

**Limitation:** The keyword-only BM25 retriever can rank passages that share common query terms above a semantically exact passage. In Q2, the exact definition from the study guide was S5, behind four noisier passages. The small corpus and top-five context still allowed a correct answer, but this ranking is unlikely to scale well.

**Proposed improvement:** Add a fully local embedding retriever or a local reranking stage, keep source and locator metadata unchanged, and evaluate it against this fixed question set. A hybrid score that combines BM25 with semantic similarity should improve paraphrase retrieval while retaining exact-term performance and offline operation.
