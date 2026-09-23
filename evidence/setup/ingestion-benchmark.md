# Fresh Ingestion Benchmark

Date: 2026-09-22 PDT

## Procedure

A clean temporary project directory was populated with unchanged copies of the three public Markdown sources. The command below created a new SQLite FTS5 index without loading the language model:

```bash
/usr/bin/time -l .venv/bin/wiki --project-root ../../work/ingest-benchmark ingest --index-only
```

## Actual Result

```text
{
  "sources_found": 3,
  "sources_changed": 3,
  "chunks_written": 176
}
0.08 real         0.06 user         0.01 sys
37617664 maximum resident set size
25674232 peak memory footprint
```

This measurement covers document discovery, Markdown parsing, chunking, hashing, SQLite schema creation, and FTS5 indexing. It intentionally excludes wiki-note generation so retrieval ingestion can be measured independently from model generation.

## Idempotence Check

A subsequent ingestion against the project index returned:

```json
{
  "sources_found": 3,
  "sources_changed": 0,
  "chunks_written": 0
}
```

The three reviewed concept-note files retained the same names and were not regenerated, demonstrating that unchanged inputs do not create duplicate notes.
