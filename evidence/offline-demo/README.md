# Complete Offline Demonstration

> Historical status: this is the original v1 evidence. The current post-context-budget run is indexed in [`../offline-context-budget/README.md`](../offline-context-budget/README.md).

> **Historical v1 evidence.** This demonstration was produced by the code at commit `e64bdfc`. It is preserved unchanged as audit history and is superseded by the v2 demonstration in [`../offline-demo-v2/README.md`](../offline-demo-v2/README.md).

Date: 2026-09-22 PDT (2026-09-23 UTC)

This demonstration ran the project in a clean local clone while macOS denied every network operation to the entire process tree. The clean clone protected the reviewed submission vault from being overwritten during the fresh model-backed ingestion test.

The outer command used this sandbox policy:

```bash
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  ./scripts/run_offline_demo.sh DEMO_ROOT WIKI_BIN PYTHON_BIN
```

The script also set `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_HUB_DISABLE_TELEMETRY=1`. Its first operation attempted a network connection and received `NETWORK_BLOCKED` before any assignment command ran.

## Full Transcript

The complete command-by-command terminal transcript is [`offline-full-session.txt`](../recordings/offline-full-session.txt). It contains:

1. the failed network probe;
2. `wiki --help`;
3. fresh, model-backed `wiki ingest ./vault/raw`;
4. repeated ingestion showing zero changes and zero new chunks;
5. `wiki status` showing three documents and 176 passages;
6. all four fixed ask-mode questions;
7. casual chat, drafting, and the “Make that shorter” follow-up;
8. explicit note retrieval in chat;
9. raw search output;
10. a chat-only fact followed by an independent ask-mode rejection.

## Full Ingestion Measurement

Fresh ingestion processed three sources, wrote 176 passages, and generated three wiki-note drafts with local Gemma.

- Wall time: `95.26 seconds`
- Maximum resident set size: `5,399,969,792 bytes` (approximately `5.40 GB`)
- Peak memory footprint reported by macOS: `5,909,975,240 bytes`
- Network access: denied by the operating-system sandbox

The immediate second ingestion returned `sources_changed: 0` and `chunks_written: 0`.

## Four Fixed Ask Tests

- Q1 — agent anatomy: [`20260923T051741822234Z-ask.md`](runs/20260923T051741822234Z-ask.md)
- Q2 — context and memory: [`20260923T051756564232Z-ask.md`](runs/20260923T051756564232Z-ask.md)
- Q3 — model versus harness bottleneck: [`20260923T051814816080Z-ask.md`](runs/20260923T051814816080Z-ask.md)
- Q4 — unsupported market revenue: [`20260923T051818429817Z-ask.md`](runs/20260923T051818429817Z-ask.md)

Each card records the exact model, local execution mode, retrieved passages and paths, actual answer, citations, and generation metrics.

## Mode-Boundary Evidence

- Capability explanation without retrieval: [`20260923T051828138943Z-chat.md`](runs/20260923T051828138943Z-chat.md)
- Draft without retrieval: [`20260923T051841680188Z-chat.md`](runs/20260923T051841680188Z-chat.md)
- Conversational shortening without retrieval: [`20260923T051849524126Z-chat.md`](runs/20260923T051849524126Z-chat.md)
- Explicit note retrieval with citations: [`20260923T051910680828Z-chat.md`](runs/20260923T051910680828Z-chat.md)
- Raw search with no model: [`20260923T051910879741Z-search.md`](runs/20260923T051910879741Z-search.md)
- Temporary fact introduced in chat: [`20260923T051917440812Z-chat.md`](runs/20260923T051917440812Z-chat.md)
- Follow-up recalls the temporary fact: [`20260923T051920330081Z-chat.md`](runs/20260923T051920330081Z-chat.md)
- Independent ask cannot use the chat-only fact: [`20260923T051924078743Z-ask.md`](runs/20260923T051924078743Z-ask.md)

## Reproduction

The checked-in [`scripts/run_offline_demo.sh`](../../scripts/run_offline_demo.sh) contains the exact sequence. It requires a prepared local model cache and a clean project copy containing the source documents and configuration files.
