# Network-Isolated Verification

Date: 2026-09-22 PDT

The final offline check used both library-level offline flags and an operating-system sandbox policy that denied all network access to the command:

```bash
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  /usr/bin/env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
  .venv/bin/wiki ask "What are the two main parts of an AI agent?" --mode local
```

The command exited successfully and produced a complete cited answer:

```text
Model: mlx-community/gemma-4-e4b-it-4bit | Execution: local
An AI agent is composed of two main parts [S1]:

1. The Brain (AI Model): This component handles all the thinking, including reasoning and planning, and determines which Actions to take based on the current situation [S1].
2. The Body (Capabilities and Tools): This represents everything the Agent is equipped to do, and the scope of possible actions is determined by what the agent has been equipped with [S1].
```

The machine remained connected for documentation work, but the tested process had no network capability. The model snapshot, source documents, index, prompts, and inference runtime were all read locally. The complete retrieved passages and measured generation metrics are saved in [`../runs/20260923T043603863616Z-ask.md`](../runs/20260923T043603863616Z-ask.md).

A second network-denied run was captured as a terminal transcript at [`../recordings/offline-session.txt`](../recordings/offline-session.txt). It also completed successfully with a cited answer.
