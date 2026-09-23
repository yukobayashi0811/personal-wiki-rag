# Evaluation Results

Evaluation date: 2026-09-22 PDT (2026-09-23 UTC)

All final model-backed checks used `mlx-community/gemma-4-e4b-it-4bit` through MLX-LM 0.31.3. The model and all evidence were local. The fixed questions and pass conditions are defined in [`questions.md`](questions.md).

## Fixed Ask Questions

| Question | Result | Evidence | Assessment |
| --- | --- | --- | --- |
| Q1: Agent anatomy | Pass | [`20260923T043603863616Z-ask.md`](../evidence/runs/20260923T043603863616Z-ask.md) | Identified the model as the brain and capabilities/tools as the body. All claims cite S1. This run also passed with operating-system network access denied. |
| Q2: Context and memory | Pass | [`20260923T043104225188Z-ask.md`](../evidence/runs/20260923T043104225188Z-ask.md) | Correctly defined current-call context and saved-for-later memory. Both definitions cite S5, the relevant study-guide passage. |
| Q3: Model versus harness bottleneck | Pass after one diagnosed generation failure | [`20260923T043221749943Z-ask.md`](../evidence/runs/20260923T043221749943Z-ask.md) | Correctly described a controlled model swap and interpreted small versus large score changes. The answer also distinguished model swapping from ablation. |
| Q4: Unsupported market revenue | Pass | [`20260923T043248381896Z-ask.md`](../evidence/runs/20260923T043248381896Z-ask.md) | Returned the exact insufficient-evidence response instead of guessing. |

The first Q3 attempt ended mid-sentence after using the original 700-token generation budget. The failed record is retained at [`20260923T043130284355Z-ask.md`](../evidence/runs/20260923T043130284355Z-ask.md). Retrieval had selected the correct passage, so the fault was isolated to generation. Increasing the default budget to 1,400 tokens produced the complete passing answer above.

## Mode-Boundary Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Capability question does not trigger retrieval | Pass; zero passages retrieved | [`20260923T043323841940Z-chat.md`](../evidence/runs/20260923T043323841940Z-chat.md) |
| Drafting request does not trigger retrieval | Pass; zero passages retrieved | [`20260923T043337450324Z-chat.md`](../evidence/runs/20260923T043337450324Z-chat.md) |
| Follow-up uses chat history | Pass; “Make that shorter” condensed the immediately preceding plan with zero retrieval | [`20260923T043344882282Z-chat.md`](../evidence/runs/20260923T043344882282Z-chat.md) |
| Explicit note request triggers retrieval and citations | Pass; five passages retrieved and factual claims cite S1 | [`20260923T043401665161Z-chat.md`](../evidence/runs/20260923T043401665161Z-chat.md) |
| Search returns raw text and source locations without generation | Pass; model is recorded as not used | [`20260923T043413510666Z-search.md`](../evidence/runs/20260923T043413510666Z-search.md) |
| Ask cannot use a fact introduced only in chat | Pass; chat retained “teal,” while a separate ask returned insufficient evidence | [`20260923T043453571040Z-chat.md`](../evidence/runs/20260923T043453571040Z-chat.md), [`20260923T043456921513Z-chat.md`](../evidence/runs/20260923T043456921513Z-chat.md), [`20260923T043505609105Z-ask.md`](../evidence/runs/20260923T043505609105Z-ask.md) |

## Performance Measurements

- Fresh local indexing of three sources produced 176 passages in 0.08 seconds with a maximum resident set size of 37,617,664 bytes. See [`ingestion-benchmark.md`](../evidence/setup/ingestion-benchmark.md).
- The network-isolated Q1 answer completed in 10.63 seconds. Process resident memory rose from 4.685 GB to 4.700 GB while the already-loaded model generated the answer.
- The longest passing fixed answer, Q3, completed in 20.69 seconds and ended at 4.700 GB process resident memory.

## Observed Limitation and Improvement

**Limitation:** The keyword-only BM25 retriever can rank passages that share common query terms above a semantically exact passage. In Q2, the exact definition from the study guide was S5, behind four noisier passages. The small corpus and top-five context still allowed a correct answer, but this ranking is unlikely to scale well.

**Proposed improvement:** Add a fully local embedding retriever or a local reranking stage, keep source and locator metadata unchanged, and evaluate it against this fixed question set. A hybrid score that combines BM25 with semantic similarity should improve paraphrase retrieval while retaining exact-term performance and offline operation.
