# Submission Checklist

This checklist maps assignment requirements to repository evidence. A checked item must be supported by a committed file.

## Repository and Runtime

- [x] Public repository: [yukobayashi0811/personal-wiki-rag](https://github.com/yukobayashi0811/personal-wiki-rag)
- [x] Custom CLI implements chat, ask, search, ingest, status, and help.
- [x] Local model configuration pins mlx-community/gemma-4-e4b-it-4bit and MLX-LM 0.31.3.
- [x] Model weights, credentials, local database, and working drafts are excluded from Git.

## Sources and Wiki

- [x] Three unchanged originals are committed under [vault/raw/](../vault/raw/).
- [x] Provenance, revision, license, and SHA-256 values are documented in [SOURCES.md](SOURCES.md).
- [x] Source summaries and subject-level concept notes use distinct folders and vault-root links.
- [x] index.md is grouped by frontmatter topic and provides a navigation path to notes and originals.
- [x] Automated tests require every authored wikilink to resolve to exactly one file.
- [x] The repository owner confirmed review of every v2 note against the originals; all six notes are marked reviewed: true.

Review instructions: [HUMAN-STEPS.md](HUMAN-STEPS.md).

## Safe Ingestion

- [x] Every model draft is written to ignored data/drafts/.
- [x] Reviewed, curated, protected legacy, and non-generated notes are not overwritten.
- [x] An unreviewed generated note updates in place without duplication.
- [x] Removed sources and their chunks are deleted from the index.
- [x] The ingest summary reports removed sources, drafts, created notes, protected notes, and truncated sources.
- [x] The final sandboxed changed-source demonstration is committed and indexed.

## Modes and Evaluation

- [x] Ask and chat prompts and histories remain separated.
- [x] Search works without importing MLX-LM.
- [x] Chat supports deterministic automatic retrieval and /notes <query>.
- [x] Chat history is bounded by WIKI_CHAT_TURNS, default 12.
- [x] The fixed Q1-Q4 questions and pass conditions remain unchanged.
- [x] The v2 fixed-question results and claim-by-claim citation assessment are committed.

## Offline Evidence

- [x] The v1 demonstration remains available as historical evidence.
- [x] The v2 wrapper records the exact command, commit, UTC time, outside DNS/TCP success, and inside DNS/TCP failure.
- [x] The v2 inner script covers ingestion, repeat ingestion, all fixed questions, chat boundaries, search, ask/chat separation, and changed-source re-ingestion.
- [x] The complete v2 transcript ends with OFFLINE_DEMO_V2_COMPLETE.
- [x] Unedited screen captures of the committed transcript document the v2 control probe, sandbox isolation, core commands, and completion; they are explicitly labeled as transcript views rather than an original Terminal recording.
- [x] Updated Obsidian screenshots show properties, expanded folders, readable graph labels, and source navigation.

## Documentation and Measurements

- [x] README documents setup, model choice, E2B non-benchmark status, architecture, retrieval scope, review flow, chat rule, and limitations.
- [x] Measurement definitions distinguish generation time, end-to-end wall time, RSS, macOS peak footprint, and MLX peak memory.
- [x] Evidence cards record repair status, generation metrics, wall time, cited sources, structural validation, and citation mapping.
- [x] Development v1 runs are cataloged in [evidence/runs/README.md](../evidence/runs/README.md).
- [x] README and evaluation results contain only values copied from committed v2 evidence.

## Final Verification

- [x] Full test suite passes after the final evidence and documentation changes: 24 passed.
- [x] Every scoped authored Markdown link resolves; links embedded in unchanged upstream sources and verbatim retrieved passages are outside this check.
- [x] vault/raw/ SHA-256 values match docs/SOURCES.md.
- [x] Demonstration scripts pass zsh -n.
- [x] The submitted branch contains every intended change and the pull request links every v2 artifact; the repository owner's local Obsidian workspace state is intentionally excluded.
