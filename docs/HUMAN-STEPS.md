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

## 2. Capture Updated Obsidian Screenshots

Open the repository's `vault/` directory as an Obsidian vault and save these exact files:

1. `evidence/screenshots/obsidian-note-v2.png`
   - Show one subject note.
   - Keep its frontmatter properties visible.
   - Show its source link and meaningful related-note links.
2. `evidence/screenshots/obsidian-index-v2.png`
   - Expand both `raw/` and `wiki/` in the file explorer.
   - Show `index.md` beside the expanded explorer.
3. `evidence/screenshots/obsidian-graph-v2.png`
   - Use the filter `path:wiki OR file:index`.
   - Disable attachments.
   - Zoom until labels are readable.
   - Move the pointer away from every label before capturing.
4. `evidence/screenshots/obsidian-source-navigation-v2.png`
   - Click a note's source link.
   - Capture the unchanged raw source open in Obsidian.

Do not edit or composite the screenshots after capture.

## 3. Commit the Human Review

```bash
git add vault/wiki evidence/screenshots
git commit -m "Complete human note review and refresh Obsidian evidence"
git push
```

Before committing, verify that `vault/raw/` is unchanged and that no private information or absolute personal path appears in the screenshots.
