# Personal Wiki with Local Gemma and RAG

This project implements an offline command-line personal wiki for learning and researching AI-agent fundamentals. It uses a local, open-weight Gemma model through MLX-LM, a SQLite FTS5 retrieval index, explicit mode-specific prompts, source citations, and saved evidence records.

Public repository: [github.com/yukobayashi0811/personal-wiki-rag](https://github.com/yukobayashi0811/personal-wiki-rag)

## Project Status

The required CLI modes, local retrieval index, three-source wiki, fixed evaluation set, complete network-isolated demonstration, and Obsidian evidence are complete. The final index contains 3 documents and 176 passages. All saved outputs are from actual local runs; no sample answers are presented as evaluation results.

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
- Available system memory observed after model setup: 82% free.
- Free disk space observed after the model download: 19 GiB.

The E4B model was selected because the device has enough unified memory for the 4-bit model plus prompt context, retrieval, and operating-system overhead. It provides more capacity than E2B while avoiding the substantially larger storage and memory footprint of the 26B A4B model. Final memory and response-time measurements use the real wiki sources and are recorded in the evaluation results.

The initial local smoke test generated a short answer in 1.18 seconds with approximately 4.69 GB of process resident memory. See [`evidence/setup/model-smoke-test.md`](evidence/setup/model-smoke-test.md). In the final network-isolated evaluation, full model-backed ingestion took 95.26 seconds and reached approximately 5.40 GB maximum resident memory. Q1 completed in 10.89 seconds and ended at 4.70 GB process resident memory.

## Architecture

The [`CLI`](src/personal_wiki/cli.py) is the user-facing command layer. The [`harness`](src/personal_wiki/harness.py) selects a mode, loads the correct instructions, controls conversation context, decides whether chat requires retrieval, calls the [`retrieval store`](src/personal_wiki/store.py), assembles prompts, invokes [`local Gemma`](src/personal_wiki/model.py), validates citation markers, handles expected errors, and saves evidence through [`evidence.py`](src/personal_wiki/evidence.py).

The retrieval tool is independent of the model. It extracts local Markdown, text, or PDF sources into passages, preserves source paths and page or section locators, and searches them with SQLite FTS5. Search mode stops after returning those original passages. Ask mode supplies retrieved passages to Gemma as non-parametric context. This is retrieval-augmented generation, not model training.

One ask-mode path is:

1. `wiki ask` parses the standalone question and displays the configured model and local execution setting.
2. The harness asks SQLite FTS5 for the top five original passages.
3. The prompt builder combines research rules, the question, passage text, filenames, section locators, and temporary `[S#]` labels.
4. MLX-LM loads the cached Gemma snapshot and generates locally.
5. The harness checks that cited markers refer to supplied passages, attempts one repair if markers are missing or invalid, and otherwise returns the insufficient-evidence response.
6. The CLI displays the answer while the evidence writer saves the input, retrieved passages, exact model, output, and timing and memory metrics.

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

Requirements: an Apple Silicon Mac, Python 3.11 or later, sufficient local disk space for the model, and internet access only for the initial dependency and model download.

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Download the exact model while online, or allow the first model-backed command to download it:

```bash
source .venv/bin/activate
hf download mlx-community/gemma-4-e4b-it-4bit
wiki status
wiki ingest ./vault/raw
```

Model weights are stored in the local Hugging Face cache and must not be committed. The default model, generation budget, and retrieval depth can be overridden with `WIKI_MODEL`, `WIKI_MAX_TOKENS`, and `WIKI_TOP_K`. The submitted evaluation uses the defaults recorded in [`config/model.json`](config/model.json).

## Source Preparation

Place at least three shareable `.md`, `.txt`, or text-extractable `.pdf` files in `vault/raw/`. Originals are read but never rewritten. Use files that may legally and safely be included in a public repository; remove private information before ingestion.

This repository uses three open-license AI-agent sources. See [`docs/SOURCES.md`](docs/SOURCES.md) for exact provenance, revisions, licenses, checksums, and selection rationale:

- `AI Agent Fundamentals.md` — Hugging Face Agents Course;
- `AI Agents Study Guide.md` — Microsoft AI Agents for Beginners;
- `Evaluating AI Agents.md` — *Understanding AI Agent*, Chapter 7.

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

## Design Choices

- **Passages:** Markdown headings and PDF pages provide locators. Text is grouped toward 1,200 characters with 180 characters of overlap. The complete sources are indexed; wiki-note generation supplies Gemma with at most 24,000 source characters per document.
- **Retrieval:** SQLite FTS5 with Porter stemming performs local BM25 ranking. Queries use important terms with OR matching, and the default top five passages retain their original filename and locator.
- **Prompts:** [`wiki-instructions.md`](config/wiki-instructions.md) restricts factual answers to retrieved evidence. [`persona.md`](config/persona.md) gives chat a recognizable but bounded assistant voice. Ask never receives the chat persona or chat history.
- **Chat context:** Conversation history exists only inside the current `wiki chat` process. The current implementation retains all turns from that session and does not persist them. Retrieval is triggered by explicit references to notes, the wiki, sources, documents, or citations.
- **Model generation:** Ask uses temperature 0.1, chat uses 0.5, wiki-note drafts use 0.2, and the default generation budget is 1,400 tokens. The budget was raised from 700 after a real Q3 answer ended mid-sentence; both records are retained.
- **Names and folders:** Original sources remain in `vault/raw/`. Reviewed subject notes use matching two-to-four-word filenames and H1 headings in `vault/wiki/Concepts/`. `vault/index.md` is the human landing page. Machine chunks and IDs remain in `data/` and evidence files outside the vault.
- **Source mapping:** Human notes link back to unchanged source filenames. Retrieval assigns `[S1]` through `[S5]` per query and records the corresponding filename, locator, text, and score in each evidence card.
- **Re-ingestion:** SHA-256 hashes identify unchanged sources. Unchanged files are not re-chunked or regenerated; changed sources replace their indexed chunks instead of adding duplicates. The final offline run confirms a second ingestion writes zero new chunks.

## Evaluation

The fixed questions and pass conditions are in [`evaluation/questions.md`](evaluation/questions.md). The assessed results, metrics, mode-boundary checks, observed limitation, and proposed improvement are in [`evaluation/results.md`](evaluation/results.md).

The complete requirement-to-evidence mapping is in [`docs/SUBMISSION-CHECKLIST.md`](docs/SUBMISSION-CHECKLIST.md).

Final results:

- Three answerable questions passed with source citations.
- The unsupported market-revenue question returned the exact insufficient-evidence response.
- Chat followed a drafting request with “Make that shorter” while using no retrieval.
- Chat retrieved and cited the wiki only when the user explicitly asked about notes.
- Search returned original passages and locations without loading the model.
- A personal fact introduced only in chat was not available to a separate ask command.
- Repeated ingestion detected zero changed sources and wrote zero new chunks.

## Complete Offline Evidence

One macOS sandbox session denied all network access to the CLI and every child process. A connection probe failed before the assignment commands ran. The same session then completed full ingestion, repeat ingestion, all four ask tests, chat and follow-up checks, explicit note retrieval, raw search, and ask/chat-history separation.

- [Complete offline demonstration index](evidence/offline-demo/README.md)
- [Full command-by-command terminal transcript](evidence/recordings/offline-full-session.txt)
- [Q1: Agent anatomy](evidence/offline-demo/runs/20260923T051741822234Z-ask.md)
- [Q2: Context and memory](evidence/offline-demo/runs/20260923T051756564232Z-ask.md)
- [Q3: Model versus harness bottleneck](evidence/offline-demo/runs/20260923T051814816080Z-ask.md)
- [Q4: Unsupported market revenue](evidence/offline-demo/runs/20260923T051818429817Z-ask.md)
- [Capability chat](evidence/offline-demo/runs/20260923T051828138943Z-chat.md)
- [Drafting chat](evidence/offline-demo/runs/20260923T051841680188Z-chat.md)
- [“Make that shorter” follow-up](evidence/offline-demo/runs/20260923T051849524126Z-chat.md)
- [Explicit note retrieval](evidence/offline-demo/runs/20260923T051910680828Z-chat.md)
- [Raw search without generation](evidence/offline-demo/runs/20260923T051910879741Z-search.md)
- [Ask/chat-history separation](evidence/offline-demo/runs/20260923T051924078743Z-ask.md)

## Visual Evidence

### Topic Index

![Obsidian topic index](evidence/screenshots/obsidian-index.png)

### Reviewed Note and Source Links

![Obsidian reviewed note](evidence/screenshots/obsidian-note.png)

![Obsidian source and related-note links](evidence/screenshots/obsidian-note-source.png)

### Wiki Graph

![Obsidian graph limited to the reviewed wiki and index](evidence/screenshots/obsidian-graph.png)

The saved graph filter is `path:wiki OR file:index`; attachments are disabled. From `index.md`, a reader can open a concept note, follow either related-note link, and follow the source link back to the unchanged evidence in `vault/raw/`.

## Known Limitation

The current retriever uses local BM25 keyword matching. It is transparent, fast, and completely offline, but a semantically exact passage can rank behind passages with more surface-term overlap. In Q2, the correct definition appeared as S5 behind four noisier passages. A local embedding retriever or reranker is the next concrete improvement; it should be evaluated against the same fixed questions before replacing the current implementation.

## Safety and Submission Notes

Do not commit model weights, credentials, private documents, the local database, or unredacted private information. The public repository was checked without GitHub authentication after publication; its README, code, wiki, sources, and evidence are accessible.

## Model Sources

- [Google Gemma documentation](https://ai.google.dev/gemma/docs/core)
- [MLX-LM repository](https://github.com/ml-explore/mlx-lm)
- [MLX Gemma E4B instruction-tuned 4-bit model](https://huggingface.co/mlx-community/gemma-4-e4b-it-4bit)
