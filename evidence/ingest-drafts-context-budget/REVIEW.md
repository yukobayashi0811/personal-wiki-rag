# Context-Budget Draft Review

These three Markdown files are the verbatim Gemma drafts copied from the completed network-sandboxed run at commit `08e70587ad8c6445a55485c540446e63385e740a`. They are evidence only and were not copied into `vault/wiki/`, because reviewed wiki notes require repository-owner approval.

## Review Method

The drafts were compared with the unchanged files in `vault/raw/`. Token counts below use the same MLX-LM tokenizer wrapper as ingestion.

| Draft | Output tokens | Complete required sections? | Review result |
| --- | ---: | --- | --- |
| `AI Agent Fundamentals.md` | 391 | Yes | Complete prose; the former mid-sentence ending is gone. |
| `AI Agents Study Guide.md` | 377 | Yes | Covers architecture, context, memory, retrieval, orchestration, observability, security, and evaluation. |
| `Evaluating AI Agents.md` | 645 | Yes | Includes material from the beginning, middle, and latter part of the source. |

## Largest-Source Coverage

The generated `Evaluating AI Agents.md` draft contains the following source-backed latter-section topics:

| Draft topic | Matching source section | Source character offset |
| --- | --- | ---: |
| Failure attribution | `Failure Attribution: Locate the First Error in a Trajectory` | 56,265 |
| End-to-end and trajectory-prefix regression tasks | `End-to-End and Trajectory-Prefix Regression Tasks` | 68,956 |
| Context accumulation and thinking-token cost | `Cost Analysis of Agent Systems` | 85,128 |
| Traces and diagnosis | `Agent Observability` | 97,202 |
| Production-oriented iteration | `From External Evaluation to Internal Evaluation` and adjacent production sections | 109,342 |

Every listed section starts after the former 24,000-character cutoff. This demonstrates that the new draft used information that the prior drafting path could not receive.

## Comparison with the Baseline

The pre-change baseline draft for `Evaluating AI Agents.md` is retained at [`../context-budget/baseline/drafts/Evaluating AI Agents.md`](../context-budget/baseline/drafts/Evaluating%20AI%20Agents.md). It summarizes early evaluation concepts but cannot cover the late source sections because only the first 24,000 characters were supplied. The baseline `AI Agent Fundamentals.md` draft also ends with `Actions: The high-level task performed,`; the new offline draft completes that distinction and its Source and Related Notes sections.

## Human Review Status

This review confirms source coverage and obvious completeness only. The repository owner must decide whether to promote any new draft into `vault/wiki/` and, if so, must review every claim before keeping `reviewed: true`. No existing reviewed note was overwritten.
