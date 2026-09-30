# Live Terminal Offline Rerun

This directory indexes the completed follow-up run captured directly from this Mac's Terminal.app on 2026-09-30 UTC. It supplements, and does not overwrite, the original v2 evidence. The run used commit `fba139c7dfd1f1e6e8b0c6723462722c941df27e`; that commit changes documentation only relative to the demonstrated v2 implementation.

The complete transcript is [`offline-terminal-rerun.txt`](../recordings/offline-terminal-rerun.txt) (SHA-256 `fedaba0ebc768a4fb272689ccb7bbeb3daa815c92a9c9974aa6c227cefcec070`). The copied Markdown and JSON cards in [`runs/`](runs/) and the three files in [`ingest-drafts-terminal-rerun/`](../ingest-drafts-terminal-rerun/) are direct outputs from the same run.

## Capture Method

The repository was cloned to a disposable local directory at the recorded commit. Its Python environment was copied inside that clone so the wrapper's existing path replacement rendered paths as `[project-root]` and `[isolated-demo-root]`. The Terminal prompt was cleared and set without a username or working directory. The visible run invoked the required wrapper through line buffering:

```text
/usr/bin/stdbuf -oL -eL ./scripts/run_offline_demo_sandboxed.sh
```

The wrapper still executed the exact `OUTER_COMMAND` recorded on transcript line 3. A display-only `awk` pipe printed every line unchanged, paused at deterministic milestones, and created temporary local marker files so captures could be timed. The wrapper wrote its transcript before that display pipe; the copied transcript is byte-identical to the wrapper output in the disposable clone.

Display sleep was prevented with `caffeinate -dimsu`. Each PNG was captured directly from the Terminal content rectangle with the macOS command below, substituting the live window bounds and destination filename:

```text
/usr/sbin/screencapture -x -t png -R<x>,<y>,<width>,<height> <output.png>
```

No image was redrawn, cropped after capture, edited, or composited. The Terminal title bar was excluded at capture time so the username was never recorded. A macOS software-update notification overlaps the upper-right edge of some captures; it remains visible because the images are unedited.

## Screenshot-to-Transcript Map

| Direct Terminal capture | Same-run transcript lines | Content shown |
| --- | --- | --- |
| [01 start and outer probes](../screenshots/offline-terminal-rerun-01-start-and-outer-probes.png) | [1-7](../recordings/offline-terminal-rerun.txt#L1-L7) | `UTC_START`, `GIT_COMMIT`, `OUTER_COMMAND`, outside DNS and TCP success |
| [02 inner network block](../screenshots/offline-terminal-rerun-02-inner-network-block.png) | [24-53](../recordings/offline-terminal-rerun.txt#L24-L53) | device/runtime details and inside DNS/TCP failures |
| [03 fresh ingest](../screenshots/offline-terminal-rerun-03-ingest.png) | [55-103](../recordings/offline-terminal-rerun.txt#L55-L103) | help prerequisites and fresh-ingest counts |
| [04 Q1](../screenshots/offline-terminal-rerun-04-q1.png) | [127-173](../recordings/offline-terminal-rerun.txt#L127-L173) | repeat ingest, status, and the first fixed answer |
| [05 Q2](../screenshots/offline-terminal-rerun-05-q2.png) | [156-198](../recordings/offline-terminal-rerun.txt#L156-L198) | context and memory definitions |
| [06 Q3](../screenshots/offline-terminal-rerun-06-q3.png) | [181-231](../recordings/offline-terminal-rerun.txt#L181-L231) | model-versus-harness answer |
| [07 Q4](../screenshots/offline-terminal-rerun-07-q4.png) | [214-253](../recordings/offline-terminal-rerun.txt#L214-L253) | exact insufficient-evidence response |
| [08 chat capabilities](../screenshots/offline-terminal-rerun-08-chat-capabilities.png) | [233-286](../recordings/offline-terminal-rerun.txt#L233-L286) | both capability prompts and concrete starting points |
| [09 chat retrieval](../screenshots/offline-terminal-rerun-09-chat-retrieval.png) | [289-325](../recordings/offline-terminal-rerun.txt#L289-L325) | suggestion follow-up plus sourced model-swap and tools answers |
| [10 forced notes](../screenshots/offline-terminal-rerun-10-forced-notes.png) | [305-332](../recordings/offline-terminal-rerun.txt#L305-L332) | forced `/notes` output and search command boundary |
| [11 changed-source re-ingest](../screenshots/offline-terminal-rerun-11-changed-source-reingest.png) | [401-437](../recordings/offline-terminal-rerun.txt#L401-L437) | chat/ask isolation, changed-source counts, protected notes, and restoration start |
| [12 restoration and completion](../screenshots/offline-terminal-rerun-12-complete.png) | [414-452](../recordings/offline-terminal-rerun.txt#L414-L452) | restored-source re-ingest and `OFFLINE_DEMO_V2_COMPLETE` |

## Differences from the Original V2 Run

The differences are retained rather than normalized:

- The original v2 run used commit `df41bf599cc53a99ee653bc19ca9db0d1871f3d1`; this capture rerun used documentation-only commit `fba139c7dfd1f1e6e8b0c6723462722c941df27e` with the same `src/`, `config/`, `scripts/`, and `tests/` content.
- Available disk was 14 GiB at 97% capacity in this run, versus 13 GiB at 97% in v2.
- Full ingest was 93.79 seconds rather than 102.96 seconds. Command-level Q1-Q4 times were 11.43, 14.36, 27.88, and 3.74 seconds, compared with 14.32, 25.04, 28.25, and 3.81 seconds in v2.
- Q1-Q4 remained substantively consistent: Q1-Q3 were cited, and Q4 returned the same exact insufficient-evidence sentence.
- Both capability responses in this rerun supplied a concrete starting point. This improves on the original v2 `What can you help me with?` output, whose assessment remains documented as partial.
- Forced `/notes context and memory` still failed to define context and memory and remained focused on memory-system implementation and evaluation. The v2 typo “Reasoning Correctiveness” did not recur. This run cited separate `[S1]` and `[S3]` markers, so its evidence card lists both; it does not remove the documented parser defect for grouped markers such as `[S1, S3]`.
- The model-swap and tools chat answers each required one recorded citation repair in this run. All three generated ingest drafts also differ byte-for-byte from the original v2 drafts, as expected from nondeterministic generation; both sets are preserved separately.

## Key Run Cards

- [Q1](runs/20260930T003456659819Z-ask.md)
- [Q2](runs/20260930T003511023861Z-ask.md)
- [Q3](runs/20260930T003538895154Z-ask.md)
- [Q4](runs/20260930T003542684345Z-ask.md)
- [`What can we do?`](runs/20260930T003604398310Z-chat.md)
- [`What can you help me with?`](runs/20260930T003622515854Z-chat.md)
- [Model-swap retrieval](runs/20260930T003724317985Z-chat.md)
- [Tools retrieval](runs/20260930T003815679244Z-chat.md)
- [Forced `/notes`](runs/20260930T003853756192Z-chat.md)
- [Search without generation](runs/20260930T003853969458Z-search.md)
