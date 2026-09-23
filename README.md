# Personal Wiki with Local Gemma and RAG

This project implements an offline command-line personal wiki. It uses a local, open-weight Gemma model through MLX-LM, a SQLite FTS5 retrieval index, explicit mode-specific prompts, source citations, and saved evidence records.

## Project Status

The CLI foundation is implemented. Source ingestion and the final wiki are intentionally pending until three shareable source documents are selected. No sample facts or invented evaluation results are used as substitutes.

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

The E4B model was selected because the device has enough unified memory for the 4-bit model plus prompt context, retrieval, and operating-system overhead. It provides more capacity than E2B while avoiding the substantially larger storage and memory footprint of the 26B A4B model. Final peak memory and response-time measurements will be recorded using the real wiki sources.

The initial local smoke test generated a short answer in 1.18 seconds with approximately 4.69 GB of process resident memory. See [`evidence/setup/model-smoke-test.md`](evidence/setup/model-smoke-test.md). This is an environment check, not the final source-backed evaluation.

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

## Evaluation Plan

Before running the final evaluation, define three answerable questions and their expected source passages, plus one plausible question that the sources cannot answer. Keep the answer key outside the searchable wiki. For every ask test, save the question, retrieved passages, actual Gemma answer, citations, model identity, local execution setting, timing, and an assessment of whether the passages support the claims.

Also verify these mode boundaries:

1. A capability question in chat does not trigger an unnecessary note search.
2. A drafting request followed by “make that shorter” uses conversation context.
3. Search returns original passages and paths without a generated answer.
4. Ask returns a cited standalone answer.
5. A claim introduced only in chat is not treated as ask-mode evidence.

The final run must occur after disconnecting the internet and restarting the CLI. It must include ingestion, all four ask tests, chat and follow-up checks, raw search, and a repeated ingestion that proves no duplicate notes are created.

## Evidence Still Required

- Three answerable ask-mode evidence cards.
- One unsupported ask-mode evidence card.
- Chat, follow-up, search, and mode-separation transcripts.
- Measured model memory use and response time for ingestion and one answer.
- Offline terminal recording or screenshots.
- Obsidian screenshots showing an open note, the topic index or page list, and a readable graph with meaningful links.
- One observed limitation and one concrete proposed improvement.

## Safety and Submission Notes

Do not commit model weights, credentials, private documents, the local database, or unredacted private information. Before submission, open the public repository while signed out and verify that the README, code, wiki, sources, and evidence links are accessible.

## Model Sources

- [Google Gemma documentation](https://ai.google.dev/gemma/docs/core)
- [MLX-LM repository](https://github.com/ml-explore/mlx-lm)
- [MLX Gemma E4B instruction-tuned 4-bit model](https://huggingface.co/mlx-community/gemma-4-e4b-it-4bit)
