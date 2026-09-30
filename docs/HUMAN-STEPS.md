# Human Review and Screenshot Record

The repository owner confirmed completion of the source review on 2026-09-29. This file preserves the procedure that was followed and records the completed screenshot set.

## 1. Review Notes and Gemma Drafts — Complete

1. Open every Markdown file in `vault/wiki/Concepts/` and `vault/wiki/Source Summaries/`.
2. Open the corresponding unchanged original in `vault/raw/`.
3. Compare each factual sentence with the named source section.
4. Review each actual Gemma draft in `evidence/ingest-drafts-v2/` against the source and its committed note.
5. Correct errors, unsupported claims, broken links, or misleading wording in the wiki note.
6. Only after completing that review, change the note's frontmatter from `reviewed: false` to `reviewed: true`.
7. For a protected legacy note, remove `ingest_protected: true` only after `reviewed: true` is present.

## 2. Updated Obsidian Screenshots — Complete

The following unedited captures were completed on 2026-09-29 and are committed under `evidence/screenshots/`:

1. `evidence/screenshots/obsidian-note-v2.png` — subject note with visible properties, related links, and source links.
2. `evidence/screenshots/obsidian-index-v2.png` — expanded `raw/`, `wiki/Concepts/`, and `wiki/Source Summaries/` beside the topic index.
3. `evidence/screenshots/obsidian-graph-v2.png` — `path:wiki OR file:index`, attachments disabled, readable labels, and pointer away from labels.
4. `evidence/screenshots/obsidian-source-navigation-v2.png` — unchanged raw source open after following the concept note's source link.
5. `evidence/screenshots/obsidian-graph-final.jpg` — direct recapture after weak cross-topic relationships were removed; the expanded folders and all seven filtered graph labels remain readable.
6. `evidence/screenshots/obsidian-note-final.jpg` — direct recapture of `Context and Memory` after its reciprocal weak relationship was removed, with review status and source links visible.

The files were saved directly from the Obsidian window and were not edited or composited.

## 3. Human Review Commit — Complete

The completed review and refreshed note capture are recorded in commit `495b22c` (`Record completed human note review`).

Before committing, verify that `vault/raw/` is unchanged and that no private information or absolute personal path appears in the screenshots. This verification is repeated in the final automated checks.

## 4. Post-Context-Budget Draft Decision — Pending

The revised ingest produced three new verbatim drafts in `evidence/ingest-drafts-context-budget/`. They were reviewed for source coverage in `REVIEW.md`, but they were intentionally not copied into `vault/wiki/`.

The repository owner has one remaining content decision:

1. Compare each new evidence draft with its reviewed note and unchanged source.
2. Either keep the current reviewed note unchanged or selectively promote source-backed improvements.
3. If a note changes, repeat the normal human claim review before retaining `reviewed: true` and refresh the relevant Obsidian screenshot only if the submitted visual should show that revision.

No code, evaluation, or offline-proof step depends on promoting these drafts.
