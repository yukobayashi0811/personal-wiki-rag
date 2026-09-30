# Context-Budget Offline Demonstration

This is the post-change offline run for the tokenizer-based wiki-draft budget. Historical v1, v2, and the earlier Terminal rerun remain unchanged in their original directories.

## Run Identity and Method

- UTC start: `2026-09-30T01:34:04Z`
- Evidence-code commit: `08e70587ad8c6445a55485c540446e63385e740a`
- Model: `mlx-community/gemma-4-e4b-it-4bit`
- MLX-LM: 0.31.3
- Invocation typed literally into Terminal.app: `./scripts/run_offline_demo_sandboxed.sh`
- Network isolation: the existing wrapper's macOS `sandbox-exec` policy with `(deny network*)`; Wi-Fi was not claimed to be disabled.
- Transcript: [`../recordings/offline-context-budget.txt`](../recordings/offline-context-budget.txt), SHA-256 `17d7e5c6cb104eb49d882d42ed485db5c3c349c0a42619f411342007ea3548af`

The outside DNS and direct-IP TCP probes succeeded. The corresponding probes failed inside the sandbox. The same sandboxed session completed fresh ingestion, unchanged re-ingestion, Q1-Q4, chat checks, forced retrieval, search, ask/chat separation, changed-source ingestion, source restoration, and a final re-ingest. It ends with `OFFLINE_DEMO_V2_COMPLETE`.

## Result Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Full-source ingest | 3/3 sources untruncated; 176 passages; 3 drafts | Transcript lines 92-135 |
| Q1 agent anatomy | Pass; cited answer | [`20260930T013632899265Z-ask.md`](runs/20260930T013632899265Z-ask.md) |
| Q2 context and memory | Pass; directly defines both terms | [`20260930T013659227500Z-ask.md`](runs/20260930T013659227500Z-ask.md) |
| Q3 model versus harness | Pass; cited model-swap procedure and interpretations | [`20260930T013728919184Z-ask.md`](runs/20260930T013728919184Z-ask.md) |
| Q4 unsupported revenue | Pass; exact insufficient-evidence response | [`20260930T013732669004Z-ask.md`](runs/20260930T013732669004Z-ask.md) |
| Capability explanations | Pass; both give concrete starting points | [`What can we do?`](runs/20260930T013759128681Z-chat.md), [`What can you help me with?`](runs/20260930T013817688451Z-chat.md) |
| Drafting and follow-up | Pass; no retrieval; both labeled `Suggestion` | [`initial`](runs/20260930T013837228756Z-chat.md), [`follow-up`](runs/20260930T013851603158Z-chat.md) |
| Automatic knowledge retrieval | Pass for model swap and tools | [`model swap`](runs/20260930T013941464751Z-chat.md), [`tools`](runs/20260930T014043138374Z-chat.md) |
| Forced `/notes` | Retrieval pass; answer-quality limitation remains | [`20260930T014121627144Z-chat.md`](runs/20260930T014121627144Z-chat.md) |
| Search | Pass; original passages; no model | [`20260930T014121805481Z-search.md`](runs/20260930T014121805481Z-search.md) |
| Ask/chat separation | Pass | [`chat introduction`](runs/20260930T014132163214Z-chat.md), [`chat recall`](runs/20260930T014138236076Z-chat.md), [`separate ask`](runs/20260930T014142105047Z-ask.md) |
| Changed/restored source | Pass; reviewed note protected and no truncation | Transcript lines 441-493 |

The forced `/notes context and memory` answer again discusses the role and implementations of memory without giving the concise definitions requested. Its grouped citations also reproduce the disclosed citation-card parsing limitation. This is not scored as an answer-quality pass.

## Direct Terminal.app Captures

All PNGs below are direct, unedited macOS captures of the Terminal.app window that ran the command above. They were not reconstructed from transcript text, converted from HTML, composited, or annotated. Capture 01 was taken while the command was running before the wrapper's buffered output appeared; capture 02 was taken later during the live run. Captures 04-17 show the same Terminal window's original scrollback after completion. The capture command was `/usr/sbin/screencapture -x -t png -R...`; the region height was reduced for some scrollback captures so no user name or full local path appeared.

| Image | What is visible | Matching transcript lines |
| --- | --- | --- |
| [`01-start-network.png`](../screenshots/offline-context-budget-01-start-network.png) | Literal command while it was executing | Invocation that produced lines 1-493 |
| [`04-metadata-probes.png`](../screenshots/offline-context-budget-04-metadata-probes.png) | UTC start, commit, outer command, outside probes, device and disk | 1-26 |
| [`05-inner-network.png`](../screenshots/offline-context-budget-05-inner-network.png) | Cached snapshot, blocked DNS/TCP, help start | 48-68 |
| [`06-ingest-token-budget.png`](../screenshots/offline-context-budget-06-ingest-token-budget.png) | Source and prompt token counts; no truncation | 96-117 |
| [`07-ingest-metrics.png`](../screenshots/offline-context-budget-07-ingest-metrics.png) | Full ingest time, RSS, peak footprint, zero swaps | 118-135 |
| [`08-q1.png`](../screenshots/offline-context-budget-08-q1.png) | Q1 and answer | 153-169 |
| [`09-q2.png`](../screenshots/offline-context-budget-09-q2.png) | Q2 answer and metrics | 187-210 |
| [`10-q3-start.png`](../screenshots/offline-context-budget-10-q3-start.png) | Q3 question and model-swap procedure | 205-220 |
| [`11-q3-result.png`](../screenshots/offline-context-budget-11-q3-result.png) | Q3 interpretations and metrics | 220-245 |
| [`12-q4.png`](../screenshots/offline-context-budget-12-q4.png) | Q4 insufficient-evidence response | 240-255 |
| [`13-chat-capabilities.png`](../screenshots/offline-context-budget-13-chat-capabilities.png) | Chat inputs and capability explanation | 270-286 |
| [`02-chat-retrieval.png`](../screenshots/offline-context-budget-02-chat-retrieval.png) | Suggestion follow-up plus cited model-swap and tools answers | 313-351 |
| [`14-forced-notes.png`](../screenshots/offline-context-budget-14-forced-notes.png) | Forced `/notes` invocation and answer | 339-359 |
| [`15-search.png`](../screenshots/offline-context-budget-15-search.png) | `/notes` tail and original-passage search | 357-378 |
| [`16-separation.png`](../screenshots/offline-context-budget-16-separation.png) | Chat memory retained; separate ask refuses it | 427-442 |
| [`17-changed-reingest.png`](../screenshots/offline-context-budget-17-changed-reingest.png) | Changed-source token budget and protected note | 443-460 |
| [`03-reingest-complete.png`](../screenshots/offline-context-budget-03-reingest-complete.png) | Restored-source re-ingest and completion marker | 461-493 |

## Output Differences from the Previous V2 Run

- Q1-Q4 conclusions are unchanged. Q2 again retrieved the exact definitions and answered them directly.
- Both capability answers now provide concrete starting points.
- The forced `/notes` output no longer contains the old “Reasoning Correctiveness” typo, but it still does not directly define context and memory.
- Fresh ingest now reports token counts and no truncated sources. Its full-source drafts differ from v2 because the model received more source text and a larger output budget.

The observed differences are preserved as new model outputs; no prior evidence was overwritten.
