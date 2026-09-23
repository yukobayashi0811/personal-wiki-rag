# Submission Checklist

This checklist maps each assignment requirement to the submitted implementation or evidence. All repository content and deliverables are in English.

## Repository and Runtime

- [x] Public GitHub repository: [yukobayashi0811/personal-wiki-rag](https://github.com/yukobayashi0811/personal-wiki-rag)
- [x] Public accessibility checked without GitHub authentication on 2026-09-22 PDT.
- [x] Local Gemma model: `mlx-community/gemma-4-e4b-it-4bit` through MLX-LM 0.31.3.
- [x] Model weights are excluded from Git; only the model identifier and cached-snapshot revision are documented.
- [x] Custom CLI and harness implement `chat`, `ask`, `search`, `ingest`, `status`, and `--help`.

Implementation: [`src/personal_wiki/`](../src/personal_wiki/) and [`config/`](../config/).

## Wiki and Sources

- [x] Three original public source documents are preserved unchanged in [`vault/raw/`](../vault/raw/).
- [x] Provenance, license, revision, checksum, and selection rationale are recorded in [`SOURCES.md`](SOURCES.md).
- [x] Three reviewed, linked concept notes are in [`vault/wiki/Concepts/`](../vault/wiki/Concepts/).
- [x] A human-readable topic index is at [`vault/index.md`](../vault/index.md).
- [x] Source links, related-note links, and topic coverage are visible in the saved Obsidian screenshots.
- [x] The graph screenshot uses `path:wiki OR file:index` with attachments disabled, so labels and intended note connections remain readable.

Visual evidence: [`obsidian-index.png`](../evidence/screenshots/obsidian-index.png), [`obsidian-note.png`](../evidence/screenshots/obsidian-note.png), [`obsidian-note-source.png`](../evidence/screenshots/obsidian-note-source.png), and [`obsidian-graph.png`](../evidence/screenshots/obsidian-graph.png).

## Fixed Evaluation

- [x] Three answerable questions and one unsupported question are defined before the final run, with expected evidence and pass conditions.
- [x] Each final ask record includes the input, exact model, local execution mode, retrieved source paths and locators, actual answer, citations, and metrics.
- [x] Q1 passed: agent brain and body.
- [x] Q2 passed: context and memory.
- [x] Q3 passed: model capability versus harness design bottleneck.
- [x] Q4 passed: exact insufficient-evidence response instead of a guess.
- [x] One earlier Q3 truncation is retained and diagnosed; the final passing rerun used the documented 1,400-token budget.

Definitions: [`evaluation/questions.md`](../evaluation/questions.md). Assessments: [`evaluation/results.md`](../evaluation/results.md). Final records: [`evidence/offline-demo/runs/`](../evidence/offline-demo/runs/).

## Mode Boundaries

- [x] `chat` answers a capability question without retrieval.
- [x] `chat` drafts a plan and follows “Make that shorter” using conversation history without retrieval.
- [x] `chat` retrieves and cites sources when notes are explicitly requested.
- [x] `search` returns original passages and locations without loading the model.
- [x] `ask` is independent of chat persona and history; a chat-only fact is unavailable to a later standalone ask.
- [x] Re-ingesting unchanged sources writes zero new chunks and does not create duplicate notes.

Evidence links are collected in the [`complete offline demonstration`](../evidence/offline-demo/README.md).

## Offline Demonstration

- [x] The final demonstration runs in a clean local project copy.
- [x] macOS denies network access to the demonstration process and every child process.
- [x] Hugging Face and Transformers offline flags are enabled.
- [x] A connection probe fails with `NETWORK_BLOCKED` before assignment commands run.
- [x] The same session runs `--help`, full model-backed ingestion, repeat ingestion, status, all four ask questions, chat checks, note retrieval, search, and ask/chat separation.
- [x] The session ends with `OFFLINE_DEMO_COMPLETE`.

Transcript: [`evidence/recordings/offline-full-session.txt`](../evidence/recordings/offline-full-session.txt). Reproduction script: [`scripts/run_offline_demo.sh`](../scripts/run_offline_demo.sh).

## README and Measurements

- [x] Exact installation and model-download commands are documented.
- [x] Device details include OS, CPU, GPU, unified RAM, observed available memory, and free disk space.
- [x] Model details include identifier, revision, instruction tuning, 4-bit quantization, runtime, and download size.
- [x] Model-selection rationale explains the E4B tradeoff on the submitted Mac.
- [x] Full ingestion time and memory are measured: 95.26 seconds and approximately 5.40 GB maximum resident memory.
- [x] Ask time and memory are measured: Q1 took 10.89 seconds and ended at 4.70 GB resident memory.
- [x] Architecture and design choices cover source-to-Gemma flow, passage size and overlap, retrieval, prompt separation, chat context, generation settings, naming, source IDs, and deduplication.
- [x] A concrete observed limitation and a local retrieval/reranking improvement are documented.

Primary documentation: [`README.md`](../README.md).

## Final Verification

- [x] Unit tests: 8 passed.
- [x] Demonstration script syntax: passed.
- [x] Git whitespace/error check: passed.
- [x] Authored local Markdown links: passed.
- [x] Twelve final JSON evidence records, including all fixed questions and model-free search, validated.
- [x] Public repository page, README, offline evidence index, evaluation results, source file, graph image, and full transcript each returned HTTP 200 without authentication.
- [x] Working tree clean after push.

