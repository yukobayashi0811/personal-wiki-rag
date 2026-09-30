# Evaluation Results

Current evaluation start: 2026-09-30 01:34:04 UTC (2026-09-29 PDT)

All current model-backed checks used `mlx-community/gemma-4-e4b-it-4bit` through MLX-LM 0.31.3. The model, index, prompts, and evidence were local. The complete set ran inside one macOS process sandbox that denied DNS and direct TCP access. The fixed questions and pass conditions are in [`questions.md`](questions.md); the complete current session is indexed in [`evidence/offline-context-budget/README.md`](../evidence/offline-context-budget/README.md).

## Current Context-Budget Rerun

| Question | Result | Evidence | Repair |
| --- | --- | --- | --- |
| Q1: Agent anatomy | Pass | [`20260930T013632899265Z-ask.md`](../evidence/offline-context-budget/runs/20260930T013632899265Z-ask.md) | None |
| Q2: Context and memory | Pass; directly defines both terms | [`20260930T013659227500Z-ask.md`](../evidence/offline-context-budget/runs/20260930T013659227500Z-ask.md) | None |
| Q3: Model versus harness bottleneck | Pass | [`20260930T013728919184Z-ask.md`](../evidence/offline-context-budget/runs/20260930T013728919184Z-ask.md) | None |
| Q4: Unsupported market revenue | Pass; exact insufficient-evidence response | [`20260930T013732669004Z-ask.md`](../evidence/offline-context-budget/runs/20260930T013732669004Z-ask.md) | None |

## Claim-by-Claim Citation Assessment (Current Run)

This is the manual check for the submission run's actual answers. The structural validator only confirms that cited markers refer to supplied passages; each row below compares a material claim with the text of the cited passage in the same evidence card.

### Q1: Agent anatomy

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| An AI agent has two main parts. | S1 | `AI Agent Fundamentals.md` — “Let's go more formal” | Yes; the passage introduces exactly two parts. |
| The brain is the AI model and handles reasoning and planning. | S1 | Same passage | Yes; stated directly. |
| The brain decides which actions to take based on the situation. | S1 | Same passage | Yes; stated directly. |
| The body is capabilities and tools, and the scope of possible actions depends on what the agent is equipped with. | S1 | Same passage | Yes; stated directly. |

### Q2: Context and memory

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| Context is the information included in the next model call. | S5 | `AI Agents Study Guide.md` — “What You Are Building Toward” | Yes; stated directly in the component table. |
| The user's goal and tool results are examples of context. | S5 | Same passage | Yes; the table's demo column gives both as the context example. |
| Memory is information saved for later use. | S5 | Same passage | Yes; stated directly. |

### Q3: Model versus harness bottleneck

| Material claim | Citation | Source and locator | Supported? |
| --- | --- | --- | --- |
| A sound evaluation system must distinguish insufficient model capability from harness design flaws. | S1 | `Evaluating AI Agents.md` — “Evaluating Agents” | Yes; stated directly. |
| The model swap experiment is “the recommended method” for telling the two apart. | S1 | Same passage | Partly. The source calls it “a common way” to tell them apart, not the recommended method. The method is supported; the word “recommended” overstates the source. |
| The procedure holds the harness constant, swaps in a stronger or weaker model, and observes how much the score moves. | S1 | Same passage | Yes; stated directly. |
| If a stronger model does not raise the score, the bottleneck is the harness. | S1 | Same passage | Yes; stated directly. |
| If a weaker model tanks the score and results swing sharply with model capability, the model itself is the bottleneck. | S1 | Same passage | Mostly. The source hedges this as “the most direct reading” and adds that further analysis is needed to know whether the task is inherently hard or the harness leans too heavily on the model's prior knowledge. The answer drops that hedge. |
| Model swapping differs from ablation, which disables a harness component. | S1 | Same passage | Yes; the passage contrasts the two experiments directly. |

### Q4: Unsupported market revenue

None of S1–S5 (`AI Agents Study Guide.md` — “Validating Deployed Agents with Smoke Tests”; `Evaluating AI Agents.md` — “Quality Control and Long-Term Maintenance”, “The Four Components of a Task Definition”, “Scope-Sensitive Document Formatting Errors”, “The Trajectory of a Real Run”) provides 2024 global AI-agent market revenue. The answer makes no factual revenue claim and returns the exact required insufficient-evidence sentence. This is a supported refusal rather than a cited answer.

### Assessment

Q1, Q2, and Q4 pass without qualification. Q3 passes its pass condition: it holds the harness constant, interprets small versus large score changes, and distinguishes model swapping from ablation, with every claim cited to the correct passage. Two wording issues are recorded rather than hidden: “recommended” overstates the source's “common way”, and the model-bottleneck interpretation omits the source's hedge. Neither introduces a fact that is absent from the source, but both show that a correct citation does not guarantee faithful wording.

## Current Run Measurements and Mode Checks

Fresh full-source ingest supplied section-body payloads of 2,008, 3,086, and 26,285 tokens respectively; no source was truncated. The unchanged raw files contain 2,112, 3,201, and 26,763 tokens. `/usr/bin/time -l` measured 134.04 seconds, 5,400,821,760 bytes maximum RSS, 7,419,793,656 bytes peak memory footprint, and zero swaps.

Both capability answers supplied concrete starting points. Automatic model-swap and tools questions retrieved and cited original passages. The forced `/notes context and memory` run again forced retrieval but did not directly define the terms, so it remains an answer-quality failure even though the retrieval check passed. Search used no model, chat remembered an in-session fact, and a separate ask command did not receive it. Full details and links are in the current evidence index.

## Historical V2 Evaluation

V2 evaluation date: 2026-09-29 PDT (2026-09-29 UTC). The following sections retain the pre-context-budget results without rewriting their model outputs or assessments.

## V2 Fixed Ask Questions

| Question | Result | Evidence | Repair |
| --- | --- | --- | --- |
| Q1: Agent anatomy | Pass | [`20260929T184251661935Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184251661935Z-ask.md) | None |
| Q2: Context and memory | Pass | [`20260929T184316710872Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184316710872Z-ask.md) | None |
| Q3: Model versus harness bottleneck | Pass | [`20260929T184344993439Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184344993439Z-ask.md) | None |
| Q4: Unsupported market revenue | Pass | [`20260929T184348907619Z-ask.md`](../evidence/offline-demo-v2/runs/20260929T184348907619Z-ask.md) | None |

## Claim-by-Claim Citation Assessment (Historical V2)

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

Additional limitations are documented in the project README: retrieval intentionally searches originals rather than edited wiki pages, and citation validation is structural, so this claim-level assessment remains necessary. In particular, `cited_source_numbers` recognizes only standalone `[S#]` markers: the grouped marker `[S1, S3]` in the forced `/notes` output results in `S3` being omitted from that card's citation list. That implementation remains unchanged. The former 24,000-character note-drafting cap is historical; the current tokenizer-based input and output budgets, exact token counts, and measured resource impact are documented in [`evidence/context-budget/README.md`](../evidence/context-budget/README.md).

## Live Terminal Capture Rerun

A later run of the unchanged implementation was captured directly from Terminal.app and is indexed in [`evidence/offline-terminal-rerun/README.md`](../evidence/offline-terminal-rerun/README.md). Q1-Q4 remained substantively consistent. Both capability responses supplied a concrete starting point in the later generation. The forced `/notes` answer no longer contained the “Reasoning Correctiveness” typo and used separate `[S1]` and `[S3]` markers, but it still did not provide the requested definitions of context and memory. These differences are additional observed outputs, not edits to the original v2 records or their assessment.
