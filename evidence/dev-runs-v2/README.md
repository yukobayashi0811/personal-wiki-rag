# v2 Chat Retrieval Development Runs

> Historical status: these calibration runs predate the tokenizer-based note-draft budget. Current submission evidence is indexed in [`../offline-context-budget/README.md`](../offline-context-budget/README.md).

These records are development runs made on the submitted Apple M5 Mac with the real local `mlx-community/gemma-4-e4b-it-4bit` model. Network access was available, so none of these files is offline evidence. The final offline evidence is stored separately under `evidence/offline-demo-v2/`.

## Threshold Selection

The deterministic rule uses a top BM25 threshold of `2.5`, after the meta/edit and agent-domain guards. Actual scores from the rebuilt 176-passage index were:

| Input | Expected retrieval | Actual top BM25 | Decision |
| --- | ---: | ---: | ---: |
| `What can you help me with?` | No | 4.5136 | No; capability guard |
| `What can we do?` | No | 1.6216 | No; capability guard |
| `Draft a three-step plan for learning AI agents.` | No | 7.9648 | No; drafting guard |
| `Make that shorter.` | No | 2.1827 | No; edit guard |
| `Help me draft a design document for my team` | No | 7.4191 | No; drafting guard |
| `My favorite color for this conversation is teal. Please remember it.` | No | 7.4686 | No; conversational guard |
| `What is an open-source license?` | No | 4.2556 | No; agent-domain guard |
| `According to my notes, what are tools?` | Yes | 7.9785 | Yes; explicit trigger |
| `Explain the model swap experiment.` | Yes | 5.9262 | Yes; threshold |
| `What is pass^k?` | Yes | 2.7180 | Yes; threshold |
| `/notes context and memory` | Yes | 4.8576 | Yes; forced command |

The threshold sits below the lowest required positive automatic case (`2.7180`) and above the low-scoring conversational edit (`2.1827`). Guards remain necessary because BM25 score magnitude alone does not distinguish a high-overlap drafting request from a request for source-backed knowledge.

## Recorded Iterations

- [`session.txt`](session.txt) is the first complete real-model pass over all required retrieval examples.
- [`session-rerun.txt`](session-rerun.txt) verifies strengthened capability and suggestion instructions. Capability answers passed; the design-document answer still failed to start with `Suggestion:`.
- [`session-rerun-2.txt`](session-rerun-2.txt) records a failed generation-based format repair that returned an empty answer.
- [`session-rerun-3.txt`](session-rerun-3.txt) records the first response-prefix experiment; it produced duplicate `Suggestion:` labels.
- [`session-rerun-4.txt`](session-rerun-4.txt) records a second response-prefix experiment; it still produced duplicate labels.
- [`session-rerun-5.txt`](session-rerun-5.txt) records the passing general solution: the final user instruction requires the exact leading label, without editing the generated answer.
- [`session-rerun-notes.txt`](session-rerun-notes.txt) records the passing `/notes` rerun after requiring a brief, directly cited response. The earlier broad and uncited response remains in the first session record.

Every Markdown and JSON evidence pair in this directory is the direct output of one of those runs. Failed records are intentionally retained.
