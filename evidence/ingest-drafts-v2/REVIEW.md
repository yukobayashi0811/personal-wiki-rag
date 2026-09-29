# V2 Gemma Draft Review

Review date: 2026-09-29 PDT

These three files are the verbatim outputs written by `wiki ingest` during the successful network-denied v2 demonstration. They were copied from the disposable demonstration clone before it was removed. They have not been edited to resemble the committed wiki notes.

The comparison below records the relationship between each actual Gemma draft and its protected v1 source summary. The repository owner subsequently confirmed direct source review on 2026-09-29, after which all six current notes were marked `reviewed: true`.

## AI Agent Fundamentals

- **Draft result:** The draft correctly identifies the model as the agent's brain, tools and capabilities as its body, and distinguishes tools from actions.
- **Material limitation:** Generation stopped in the middle of the sentence `Agents exist on a continuous`. The draft is therefore visibly incomplete.
- **Difference from the protected note:** The protected note supplies a complete agency spectrum, expands the tools/actions distinction, adds application examples, and includes source and related-note navigation.
- **Disposition:** Preserve the protected note. Do not replace it with this incomplete draft.

## AI Agents Study Guide

- **Draft result:** The draft covers the agent-versus-chatbot distinction, model, tools, knowledge, context, memory, planning, orchestration, trust, a learning path, and a small demo.
- **Difference from the protected note:** The protected note reorganizes the source into subject-oriented design areas, expands RAG, context and memory, planning, evaluation, observability, and security, and adds consistent metadata and navigation.
- **Disposition:** Preserve the protected note. Use the draft as evidence that ingestion generated a plausible starting point, not as proof that the final prose was model-authored verbatim.

## Evaluating AI Agents

- **Draft result:** The draft covers evaluation of the model-plus-harness system, comparative and ablation experiments, the model-swap experiment, four evaluation stages, Pass@k versus Pass^k, environment components, and environment types.
- **Input limitation:** Note generation received only the first 24,000 characters of the approximately 129,000-character source. The ingest transcript explicitly records this source as truncated.
- **Difference from the protected note:** The protected note is a substantial human rewrite. Its later production material—statistical analysis, regression tests, feature flags, A/B tests, and privacy-aware analytics—comes from sections beyond the draft's 24,000-character input window and therefore was not generated from this v2 prompt.
- **Disposition:** Preserve the protected note and disclose the provenance difference. Do not imply that this draft generated the full protected summary.

## Review Outcome

The successful re-ingest wrote three new drafts, reported three protected notes, and overwrote none of the protected wiki pages. The evidence supports the narrower claim that Gemma generated starting drafts and the ingestion policy preserved the existing notes. It does not support a claim that the committed v1 summaries are verbatim Gemma outputs.
