from pathlib import Path

from personal_wiki.documents import SourceDocument, SourceSection, chunk_document, readable_title


def test_chunk_document_preserves_source_locator() -> None:
    document = SourceDocument(
        path=Path("example.md"),
        relative_path="example.md",
        sha256="abc",
        sections=(SourceSection("Design", "First paragraph.\n\nSecond paragraph."),),
    )
    chunks = chunk_document(document, target_chars=20, overlap_chars=0)
    assert len(chunks) == 2
    assert all(chunk.locator == "Design" for chunk in chunks)


def test_readable_title_removes_machine_suffix() -> None:
    assert readable_title(Path("retrieval_augmented_generation-c8d92e24fd.md")) == "Retrieval Augmented Generation"

