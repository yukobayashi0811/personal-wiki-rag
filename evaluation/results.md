# Evaluation Results

V2 evaluation date: 2026-09-29 PDT (2026-09-29 UTC)

All v2 model-backed checks used `mlx-community/gemma-4-e4b-it-4bit` through MLX-LM 0.31.3. The model, index, prompts, and evidence were local. The final set ran inside one macOS process sandbox that denied DNS and direct TCP access. The fixed questions and pass conditions are in [`questions.md`](questions.md); the complete session is indexed in [`evidence/offline-demo-v2/README.md`](../evidence/offline-demo-v2/README.md).

## V2 Fixed Ask Questions

| Question | Result | Evidence | Repair |
| --- | --- | --- | --- |
| Q1: Agent anatomy | Pass | [`20260929T184251661935Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184251661935Z-ask.md) | None |
| Q2: Context and memory | Pass | [`20260929T184316710872Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184316710872Z-ask.md) | None |
| Q3: Model versus harness bottleneck | Pass | [`20260929T184344993439Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184344993439Z-ask.md) | None |
| Q4: Unsupported market revenue | Pass | [`20260929T184348907619Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184348907619Z-ask.md) | None |

## Claim-by-Claim Citation Assessment

The structural validator records whether cited markers refer to supplied passages. The following manual assessment separately checks whether each material answer claim is supported by the cited passage.

### Q1: Agent anatomy

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| An agent has two main parts. | S1 | `AI Agent Fundamentals.md` — “Let's go more formal” | Yes; the passage introduces exactly two parts. |
| The brain is the AI model and handles reasoning and planning. | S1 | Same passage | Yes; stated directly. |
| The brain selects actions based on the situation. | S1 | Same passage | Yes; stated directly. |
| The body is capabilities and tools, which bound possible actions. | S1 | Same passage | Yes; stated directly. |

### Q2: Context and memory

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| Context is information included in the next model call. | S5 | `AI Agents Study Guide.md` — “What You Are Building Toward” | Yes; stated directly. |
| The user's goal and tool results are examples of context. | S5 | Same passage | Yes; both examples appear in the passage. |
| Memory is information saved for later use. | S5 | Same passage | Yes; stated directly. |

### Q3: Model versus harness bottleneck

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| Evaluation should distinguish insufficient model capability from harness design flaws. | S1 | `Evaluating AI Agents.md` — “Evaluating Agents” | Yes; stated directly. |
| A model-swap experiment holds the harness constant and changes the model. | S1 | Same passage | Yes; stated directly. |
| If a stronger model does not improve the score, the harness is the likely bottleneck. | S1 | Same passage | Yes; stated directly. |
| If performance changes sharply with model capability, the model is the likely bottleneck. | S1 | Same passage | Yes; stated directly. |
| Model swap differs from ablation, which disables a harness component. | S1 | Same passage | Yes; the passage contrasts the two experiments. |

### Q4: Unsupported market revenue

None of S1-S5 provides 2024 global AI-agent market revenue. The answer makes no factual revenue claim and returns the required exact insufficient-evidence sentence. This is a supported refusal rather than a cited answer.

## V2 Mode-Boundary Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `What can we do?` describes chat, local retrieval, `/notes`, CLI commands, offline limits, and a concrete starting point | Pass; zero passages retrieved | [`20260929T184410108054Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184410108054Z-chat.md) |
| `What can you help me with?` describes the capabilities and limits but offers only a generic closing question, not a concrete starting point | Partial; zero passages retrieved | [`20260929T184422037906Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184422037906Z-chat.md) |
| Generic learning-plan draft avoids retrieval and identifies itself as a suggestion | Pass | [`20260929T184428776812Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184428776812Z-chat.md) |
| Follow-up uses bounded chat history and remains a suggestion | Pass | [`20260929T184431166958Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184431166958Z-chat.md) |
| In-domain model-swap question triggers retrieval | Pass; five passages; final citations valid after one recorded repair | [`20260929T184524517051Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184524517051Z-chat.md) |
| Explicit source wording triggers retrieval | Pass; five passages; citations valid | [`20260929T184543683181Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184543683181Z-chat.md) |
| `/notes` forces retrieval | Retrieval pass, answer-quality fail: five passages were retrieved, but the answer does not define context and memory, focuses on evaluation experiments, and changes “Reasoning Correctness” to “Reasoning Correctiveness.” The grouped `[S1, S3]` marker also exposes the citation-card undercount described below. | [`20260929T184622479562Z-chat.md`](../evidence/offline-demo-v2/runs/20260929T184622479562Z-chat.md) |
| Search returns original passages and locations without generation | Pass; model recorded as not used | [`20260929T184622818458Z-search.md`](../evidence/offline-demo-v2/runs/20260929T184622818458Z-search.md) |
| Chat recalls a fact from the same session, but a separate ask does not receive it | Pass | [`introduction`](../evidence/offline-demo-v2/runs/20260929T184634346865Z-chat.md), [`chat recall`](../evidence/offline-demo-v2/runs/20260929T184638805739Z-chat.md), [`separate ask`](../evidence/offline-demo-v2/runs/20260929T184642751517Z-ask.md) |

## V2 Performance Measurements

- Full model-backed ingestion completed in 102.96 seconds. `/usr/bin/time -l` reported a maximum resident set size of 5,400,821,760 bytes and a peak memory footprint of 5,913,186,504 bytes.
- Q1 end-to-end wall time was 14.000 seconds; generation was 12.037 seconds; MLX peak memory was 4.818 GB.
- Q2 end-to-end wall time was 24.692 seconds; generation was 22.796 seconds; MLX peak memory was 4.977 GB.
- Q3 end-to-end wall time was 27.919 seconds; generation was 26.038 seconds; MLX peak memory was 4.859 GB.
- Q4 end-to-end wall time was 3.570 seconds; generation was 1.706 seconds; MLX peak memory was 4.855 GB.

The evidence cards' `wall_seconds` values cover retrieval, prompt assembly, generation, citation validation, and any repair. Their `elapsed_seconds` values cover the generation call. macOS command-level timing and memory values appear only in the full transcript.

## V1 Historical Results

The original 2026-09-23 run remains intact at [`evidence/offline-demo/README.md`](../evidence/offline-demo/README.md). It is historical evidence produced before the audit fixes and is not used for the v2 assessment. Its previously diagnosed 700-token Q3 failure remains at [`20260923T043130284355Z-ask.md`](../evidence/runs/20260923T043130284355Z-ask.md).

## Observed Limitation and Improvement

The local BM25 retriever can rank passages with stronger surface-term overlap above a semantically exact passage. In v2 Q2, the exact definition was S5. A fully local embedding retriever or reranker is the next concrete improvement; it should retain source/locator metadata and be tested against the same fixed questions before adoption.

Additional limitations are documented in the project README: wiki-note drafting has a 24,000-character per-source input cap; retrieval intentionally searches originals rather than edited wiki pages; and citation validation is structural, so this claim-level assessment remains necessary. In particular, `cited_source_numbers` recognizes only standalone `[S#]` markers: the grouped marker `[S1, S3]` in the forced `/notes` output results in `S3` being omitted from that card's citation list. The implementation is unchanged here so the committed v2 evidence remains tied to the demonstrated code.
