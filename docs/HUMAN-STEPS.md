# Human Steps Before Merge

The code, local-model runs, terminal evidence, and automated checks can be completed by the implementation agent. The following content decisions still require the repository owner's direct review. Do not mark these complete until they have actually been performed.

## 1. Review Notes and Gemma Drafts

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

The files were saved directly from the Obsidian window and were not edited or composited.

## 3. Commit the Human Review

```bash
git add vault/wiki
git commit -m "Complete human note review and refresh Obsidian evidence"
git push
```

Before committing, verify that `vault/raw/` is unchanged and that no private information or absolute personal path appears in the screenshots.
