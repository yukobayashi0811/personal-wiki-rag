# Wiki Draft Context-Budget Evidence

This directory records the measurements used to replace the former 24,000-character wiki-draft input slice with a tokenizer-based limit.

## Model and Token Audit

The locally cached model snapshot is `475b9088d29754a3379866cf5aeb6b41acd313c2`. Its cached `config.json` sets `text_config.max_position_embeddings` to **131,072 tokens**. [`token-audit.json`](token-audit.json) was produced with the same MLX-LM tokenizer wrapper used by the application, not a character estimate.

| Source | Raw-file characters | Raw-file tokens | Draft payload tokens | Complete prompt tokens |
| --- | ---: | ---: | ---: | ---: |
| `AI Agent Fundamentals.md` | 8,635 | 2,112 | 2,008 | 2,226 |
| `AI Agents Study Guide.md` | 12,716 | 3,201 | 3,086 | 3,305 |
| `Evaluating AI Agents.md` | 129,319 | 26,763 | 26,285 | 26,503 |

Raw-file counts measure each unchanged original byte-decoded as UTF-8. Draft-payload counts measure exactly what ingestion sends after the existing Markdown loader turns headings into section locators and joins all section bodies; no body section is omitted. The new default source limit is 30,000 payload tokens and the note-output limit is 2,400 tokens. The largest current prompt plus the full output allowance is `26,503 + 2,400 = 28,903` tokens, leaving 102,169 tokens below the model's configured context length. Even a source at the configured 30,000-token ceiling, using the largest measured 219-token prompt overhead, would total 32,619 tokens with the output allowance.

## Timed Ingest Comparison

Both comparison runs used `/usr/bin/time -l`, the same cached model, and a fresh local index. The baseline was run from pre-change commit `f3efdc39b878efbd577b3c473ab85cb8f6dab6ee`; the final run was made from evidence-code commit `08e70587ad8c6445a55485c540446e63385e740a`.

| Run | Draft input | Wall time | Maximum RSS | Peak memory footprint | Swaps |
| --- | --- | ---: | ---: | ---: | ---: |
| [`baseline/ingest-time.txt`](baseline/ingest-time.txt) | First 24,000 characters | 94.68 s | 5,419,188,224 bytes | 5,900,341,448 bytes | 0 |
| [`full/ingest-time.txt`](full/ingest-time.txt) | Full current sources under the 30,000-token limit | 122.27 s | 5,401,460,736 bytes | 7,421,595,896 bytes | 0 |

The full-source run took 27.59 seconds longer (+29.1%). Maximum RSS was effectively unchanged (-0.33%), while macOS peak memory footprint increased by 1,521,254,448 bytes (+25.8%). It completed without swapping on the 32 GB Mac. The first exploratory implementation run is retained under [`trial-b33e95d/`](trial-b33e95d/) rather than being presented as the final measurement.

The subsequent complete sandboxed demonstration independently measured its fresh full-source ingest at 134.04 seconds, 5,400,821,760 bytes maximum RSS, 7,419,793,656 bytes peak footprint, and zero swaps. Those command-level values are in [`offline-context-budget.txt`](../recordings/offline-context-budget.txt#L92-L135).

## Draft Outcomes

- The baseline `AI Agent Fundamentals.md` draft used 294 model-tokenizer tokens and ends in the middle of the Actions bullet.
- The final standalone full-source draft uses 439 tokens and completes all required sections.
- The complete offline demonstration's `Evaluating AI Agents.md` draft uses 645 tokens and includes failure attribution, end-to-end and trajectory-prefix regression tasks, cost analysis, context accumulation, observability, and production-oriented iteration. Those source sections begin at character offsets 56,265 through 109,342, all beyond the former 24,000-character slice.
- The final observed drafts were far below the new 2,400-token output ceiling. The larger allowance removes the known 1,400-token budget constraint without forcing every answer to consume it.

The standalone final `Evaluating AI Agents.md` draft ends with the literal model artifact `<|channel>`; it is retained rather than edited. The later full offline draft does not contain that artifact. This output difference is disclosed as model variability, not hidden by normalizing the evidence.

The detailed source comparison is in [`../ingest-drafts-context-budget/REVIEW.md`](../ingest-drafts-context-budget/REVIEW.md). Generated drafts are preserved verbatim; no model output was edited.
