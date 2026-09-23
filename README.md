# Personal Wiki with Local Gemma and RAG

This project implements an offline command-line personal wiki. It uses a local, open-weight Gemma model through MLX-LM, a SQLite FTS5 retrieval index, explicit mode-specific prompts, source citations, and saved evidence records.

## Project Status

The required CLI modes, local retrieval index, three-source wiki, fixed evaluation set, offline verification, and Obsidian evidence are complete. The final index contains 3 documents and 176 passages. All saved outputs are from actual local runs; no sample answers are presented as evaluation results.

## Required Modes

- `wiki chat`: conversational personal assistant with recent conversation context and selective note retrieval.
- `wiki ask`: standalone factual question answering from retrieved evidence, with citations or an insufficient-evidence response.
- `wiki search`: original matching passages and source locations, without answer generation.
- `wiki ingest`: unchanged source ingestion, local indexing, wiki-note generation, and index maintenance.
- `wiki --help`: command and configuration help.

## Device and Model Choice

- Device: MacBook Air with Apple M5, 10 CPU cores, 10 GPU cores, and 32 GB unified memory.
- Operating system observed during setup: macOS 27.0.
- Runtime: MLX-LM 0.31.3 on Python 3.13.
- Model: `mlx-community/gemma-4-e4b-it-4bit`.
- Model format: Apple Silicon MLX conversion, instruction-tuned, 4-bit quantization.
- Download size: approximately 5.15 GB.
- Downloaded snapshot revision: `475b9088d29754a3379866cf5aeb6b41acd313c2`.

The E4B model was selected because the device has enough unified memory for the 4-bit model plus prompt context, retrieval, and operating-system overhead. It provides more capacity than E2B while avoiding the substantially larger storage and memory footprint of the 26B A4B model. Final memory and response-time measurements use the real wiki sources and are recorded in the evaluation results.

The initial local smoke test generated a short answer in 1.18 seconds with approximately 4.69 GB of process resident memory. See [`evidence/setup/model-smoke-test.md`](evidence/setup/model-smoke-test.md). In the final network-isolated evaluation, Q1 completed in 10.63 seconds and ended at 4.70 GB process resident memory.

## Architecture

The CLI is the user-facing command layer. The harness selects a mode, loads the correct instructions, controls conversation context, decides whether chat requires retrieval, calls the retrieval tool, assembles prompts, invokes local Gemma, validates citations, handles errors, and saves evidence.

The retrieval tool is independent of the model. It extracts local Markdown, text, or PDF sources into passages, preserves source paths and page or section locators, and searches them with SQLite FTS5. Search mode stops after returning those original passages. Ask mode supplies retrieved passages to Gemma as non-parametric context. This is retrieval-augmented generation, not model training.

## Repository Layout

```text
config/                 Mode-specific persona and research rules
data/                   Local retrieval index; machine data stays outside the vault
evidence/               Saved runs, screenshots, and offline demonstration files
src/personal_wiki/      CLI, harness, retrieval, model, citation, and evidence code
tests/                  Deterministic unit tests
vault/raw/              Original source files, preserved unchanged
vault/wiki/             Reviewed, linked wiki notes
vault/index.md          Human-readable topic index
```

## Setup

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

The first model-backed command downloads the configured model from Hugging Face. Complete that download before the offline demonstration. Model weights are stored in the local Hugging Face cache and must not be committed.

## Source Preparation

Place at least three shareable `.md`, `.txt`, or text-extractable `.pdf` files in `vault/raw/`. Originals are read but never rewritten. Use files that may legally and safely be included in a public repository; remove private information before ingestion.

This repository uses three open-license AI-agent sources. See [`docs/SOURCES.md`](docs/SOURCES.md) for provenance, revisions, licenses, checksums, and selection rationale.

The selected documents cover complementary layers:

1. basic agent definitions, agency, reasoning, planning, tools, and actions;
2. system architecture, RAG, context, memory, orchestration, observability, and security;
3. evaluation design, metrics, verifiers, failure attribution, and production improvement.

## Commands

```bash
wiki --help
wiki status
wiki ingest ./vault/raw
wiki search "example topic"
wiki ask "What does the source say?" --mode local
wiki chat
```

Search works without loading Gemma. Ask treats every question independently and does not import chat history or the chat persona. Chat keeps recent conversation and retrieves only when the user explicitly refers to notes, sources, documents, or citations.

## Evaluation

The fixed questions and pass conditions are in [`evaluation/questions.md`](evaluation/questions.md). The assessed results, metrics, mode-boundary checks, observed limitation, and proposed improvement are in [`evaluation/results.md`](evaluation/results.md).

Final results:

- Three answerable questions passed with source citations.
- The unsupported market-revenue question returned the exact insufficient-evidence response.
- Chat followed a drafting request with “Make that shorter” while using no retrieval.
- Chat retrieved and cited the wiki only when the user explicitly asked about notes.
- Search returned original passages and locations without loading the model.
- A personal fact introduced only in chat was not available to a separate ask command.
- Repeated ingestion detected zero changed sources and wrote zero new chunks.

The decisive offline run used a macOS sandbox policy that denied all network access to the process, in addition to Hugging Face and Transformers offline flags. It still produced a complete cited answer. See [`evidence/setup/offline-verification.md`](evidence/setup/offline-verification.md) and the saved [`offline terminal transcript`](evidence/recordings/offline-session.txt).

## Visual Evidence

### Topic Index

![Obsidian topic index](evidence/screenshots/obsidian-index.png)

### Reviewed Note and Source Links

![Obsidian reviewed note](evidence/screenshots/obsidian-note.png)

![Obsidian source and related-note links](evidence/screenshots/obsidian-note-source.png)

### Wiki Graph

![Obsidian graph limited to the reviewed wiki and index](evidence/screenshots/obsidian-graph.png)

## Known Limitation

The current retriever uses local BM25 keyword matching. It is transparent, fast, and completely offline, but a semantically exact passage can rank behind passages with more surface-term overlap. A local embedding retriever or reranker is the next concrete improvement; it should be evaluated against the same fixed questions before replacing the current implementation.

## Safety and Submission Notes

Do not commit model weights, credentials, private documents, the local database, or unredacted private information. Before submission, open the public repository while signed out and verify that the README, code, wiki, sources, and evidence links are accessible.

## Model Sources

- [Google Gemma documentation](https://ai.google.dev/gemma/docs/core)
- [MLX-LM repository](https://github.com/ml-explore/mlx-lm)
- [MLX Gemma E4B instruction-tuned 4-bit model](https://huggingface.co/mlx-community/gemma-4-e4b-it-4bit)
