# Development Run Catalog

> Historical status: these runs predate the tokenizer-based note-draft budget. Current submission evidence is indexed in [`../offline-context-budget/README.md`](../offline-context-budget/README.md).

These are development runs produced by the v1 code. They are not network-isolated unless the Notes column explicitly says so. Each run has a Markdown card and a machine-readable JSON file with the same stem.

| Stem | Mode | Input or purpose | Outcome | Notes |
| --- | --- | --- | --- | --- |
| `20260923T043049008687Z-ask` | ask | Q1: agent anatomy | Passed | First saved Q1 development run; network available. |
| `20260923T043104225188Z-ask` | ask | Q2: context and memory | Passed | Fixed evaluation development run; network available. |
| `20260923T043130284355Z-ask` | ask | Q3: model versus harness | Failed | Answer ended mid-sentence at the original 700-token budget; retained as a diagnosed failure. |
| `20260923T043221749943Z-ask` | ask | Q3: model versus harness | Passed | Previously undocumented passing rerun after the general max-token budget changed to 1,400. |
| `20260923T043248381896Z-ask` | ask | Q4: unsupported market revenue | Passed | Returned the exact insufficient-evidence response. |
| `20260923T043323841940Z-chat` | chat | Capability explanation | Passed for v1 expectations | Did not retrieve; later audit found the capability description incomplete. |
| `20260923T043337450324Z-chat` | chat | Three-step learning plan | Passed for v1 expectations | Did not retrieve; later audit found the suggestion label missing. |
| `20260923T043344882282Z-chat` | chat | “Make that shorter” | Passed | Used same-session chat history without retrieval. |
| `20260923T043401665161Z-chat` | chat | Explicit note question about tools | Passed | Retrieved five passages and cited them. |
| `20260923T043413510666Z-search` | search | `agent brain body tools` | Passed | Returned original passages without model generation. |
| `20260923T043453571040Z-chat` | chat | Introduce temporary fact “teal” | Passed | First half of the session-memory boundary check. |
| `20260923T043456921513Z-chat` | chat | Recall temporary fact | Passed | Same chat process recalled “teal.” |
| `20260923T043505609105Z-ask` | ask | Ask for chat-only favorite color | Passed | Separate ask rejected the unsupported fact. |
| `20260923T043603863616Z-ask` | ask | Q1: agent anatomy | Passed | Preliminary OS-sandboxed ask run documented in `evidence/setup/offline-verification.md`. |
| `20260923T044545467665Z-ask` | ask | Q1: agent anatomy | Passed | Second preliminary network-denied ask captured in `evidence/recordings/offline-session.txt`. |

The complete v1 network-isolated suite is kept separately in [`../offline-demo/`](../offline-demo/). The v2 suite supersedes it without deleting this history.
