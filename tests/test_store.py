from pathlib import Path

from personal_wiki.documents import Chunk, SourceDocument, SourceSection
from personal_wiki.store import WikiStore


def source(sha256: str = "one") -> SourceDocument:
    return SourceDocument(
        path=Path("rag.md"),
        relative_path="rag.md",
        sha256=sha256,
        sections=(SourceSection("Overview", "Retrieval provides non-parametric evidence."),),
    )


def test_upsert_is_idempotent_and_search_returns_original_passage(tmp_path: Path) -> None:
    chunks = [Chunk(0, "Overview", "Retrieval provides non-parametric evidence.")]
    with WikiStore(tmp_path / "wiki.db") as store:
        assert store.upsert_document(source(), chunks) is True
        assert store.upsert_document(source(), chunks) is False
        assert store.document_count() == 1
        assert store.chunk_count() == 1
        results = store.search("What does retrieval provide?")
        assert results[0].source_path == "rag.md"
        assert results[0].text == chunks[0].text


def test_changed_source_replaces_chunks_without_duplicates(tmp_path: Path) -> None:
    with WikiStore(tmp_path / "wiki.db") as store:
        store.upsert_document(source("one"), [Chunk(0, "A", "old passage")])
        store.upsert_document(source("two"), [Chunk(0, "B", "new passage")])
        assert store.document_count() == 1
        assert store.chunk_count() == 1
        assert store.search("new passage")[0].text == "new passage"

