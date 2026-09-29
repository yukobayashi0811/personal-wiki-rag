# Offline Demonstration V2

This directory indexes the successful audit rerun performed on 2026-09-29. The CLI and all of its child processes ran under macOS `sandbox-exec` with `(deny network*)`. The wrapper first ran identical control probes outside the sandbox: DNS resolution and a direct TCP connection to `1.1.1.1:443` succeeded outside, then failed inside with `gaierror` and `PermissionError` respectively.

The demonstration used commit `df41bf599cc53a99ee653bc19ca9db0d1871f3d1`, Python 3.13.15, MLX 0.32.2, MLX-LM 0.31.3, and cached snapshot `475b9088d29754a3379866cf5aeb6b41acd313c2` of `mlx-community/gemma-4-e4b-it-4bit` on an Apple M5 Mac with 32 GB unified memory.

## Primary Evidence

- [Complete unedited transcript](../recordings/offline-full-session-v2.txt) — records the exact wrapper command, commit, environment, outside and inside probes, every command, macOS timing output, changed-source test, restoration, and `OFFLINE_DEMO_V2_COMPLETE`.
- [Actual Gemma ingest drafts and review](../ingest-drafts-v2/REVIEW.md) — preserves the three verbatim drafts and documents their differences from the protected notes.
- `runs/` — machine-readable JSON evidence and matching human-readable Markdown cards from the successful session.

## Fixed Ask Evaluation

| Check | Result | Evidence |
| --- | --- | --- |
| Q1: two main agent parts | Pass; citations valid; no repair | [run](runs/20260929T184251661935Z-ask.md) |
| Q2: context and memory | Pass; citations valid; no repair | [run](runs/20260929T184316710872Z-ask.md) |
| Q3: model vs. harness bottleneck | Pass; citations valid; no repair | [run](runs/20260929T184344993439Z-ask.md) |
| Q4: unsupported market revenue | Pass; exact insufficient-evidence response | [run](runs/20260929T184348907619Z-ask.md) |

## Chat, Search, and Isolation Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `What can we do?` capability response | Complete; zero retrieval | [run](runs/20260929T184410108054Z-chat.md) |
| `What can you help me with?` capability response | Complete; zero retrieval | [run](runs/20260929T184422037906Z-chat.md) |
| Three-step learning-plan request | Starts with `Suggestion:`; zero retrieval | [run](runs/20260929T184428776812Z-chat.md) |
| `Make that shorter.` follow-up | Uses chat history, starts with `Suggestion:`; zero retrieval | [run](runs/20260929T184431166958Z-chat.md) |
| Model-swap explanation | Five passages; repair attempted; final citations valid | [run](runs/20260929T184524517051Z-chat.md) |
| Notes question about tools | Five passages; citations valid; no repair | [run](runs/20260929T184543683181Z-chat.md) |
| Forced `/notes context and memory` | Five passages; citations valid; no repair | [run](runs/20260929T184622479562Z-chat.md) |
| Raw search | Five original passages; model not used | [run](runs/20260929T184622818458Z-search.md) |
| Introduce `teal` in chat | Zero retrieval | [run](runs/20260929T184634346865Z-chat.md) |
| Recall `teal` in the same chat | Correct; zero retrieval | [run](runs/20260929T184638805739Z-chat.md) |
| Ask for favorite color separately | Exact insufficient-evidence response | [run](runs/20260929T184642751517Z-ask.md) |

`citations_valid: false` on non-retrieval chat and raw search records means citation validation was not applicable; retrieved factual chat runs and answerable ask runs record `true`.

## Ingestion Checks

- Fresh ingest: 3 changed sources, 176 current chunks, 3 drafts written, 0 new notes, 3 protected notes, and one truncated draft input.
- Immediate repeat: 0 changed sources, 0 chunks written, 0 drafts, and 0 note writes.
- Changed-source test: the disposable copy of one raw source produced 1 changed source, 11 replaced chunks, 1 draft, and 1 protected note; the wiki still contained exactly six intended note files and no duplicate.
- Restoration test: restoring the original source produced the same one-source replacement and again preserved the note.

The mutation and restoration occurred only in the disposable clone. The committed `vault/raw/` files were not changed.

## Retained Failed Attempts

Failures are retained rather than rewritten or hidden:

- [Attempt 01](../recordings/offline-full-session-v2-failed-01.txt) — the timing wrapper attempted to execute a shell function directly and stopped before model execution.
- [Attempt 02](../recordings/offline-full-session-v2-failed-02.txt) — the suite completed, but sourced chat answers did not enforce complete citation coverage; cards are in `failed-02-runs/`.
- [Attempt 03](../recordings/offline-full-session-v2-failed-03.txt) — citation enforcement worked, but the forced `/notes` response fell back to insufficient evidence; cards are in `failed-03-runs/`.

Those attempts are development history. Only `runs/` and `offline-full-session-v2.txt` are the final v2 assessment evidence.
