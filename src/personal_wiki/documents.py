from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}


@dataclass(frozen=True)
class SourceSection:
    locator: str
    text: str


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    relative_path: str
    sha256: str
    sections: tuple[SourceSection, ...]


@dataclass(frozen=True)
class Chunk:
    index: int
    locator: str
    text: str


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_markdown(path: Path) -> tuple[SourceSection, ...]:
    text = path.read_text(encoding="utf-8")
    sections: list[SourceSection] = []
    current_heading = "document"
    current_lines: list[str] = []

    def flush() -> None:
        body = "\n".join(current_lines).strip()
        if body:
            sections.append(SourceSection(current_heading, body))

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            flush()
            current_lines = []
            current_heading = re.sub(r"^#{1,6}\s+", "", line).strip()
        else:
            current_lines.append(line)
    flush()
    return tuple(sections or [SourceSection("document", text.strip())])


def _read_text(path: Path) -> tuple[SourceSection, ...]:
    text = path.read_text(encoding="utf-8")
    return (SourceSection("document", text.strip()),)


def _read_pdf(path: Path) -> tuple[SourceSection, ...]:
    reader = PdfReader(str(path))
    sections = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            sections.append(SourceSection(f"page {page_number}", text))
    if not sections:
        raise ValueError(f"No extractable text found in PDF: {path}")
    return tuple(sections)


def load_source(path: Path, raw_dir: Path) -> SourceDocument:
    path = path.resolve()
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported source type: {suffix or '[no extension]'}")
    if suffix == ".pdf":
        sections = _read_pdf(path)
    elif suffix == ".md":
        sections = _read_markdown(path)
    else:
        sections = _read_text(path)
    return SourceDocument(
        path=path,
        relative_path=path.relative_to(raw_dir.resolve()).as_posix(),
        sha256=file_sha256(path),
        sections=sections,
    )


def discover_sources(raw_dir: Path) -> list[Path]:
    if not raw_dir.exists():
        return []
    return sorted(
        path
        for path in raw_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def chunk_document(
    document: SourceDocument,
    target_chars: int = 1_200,
    overlap_chars: int = 180,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for section in document.sections:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", section.text) if part.strip()]
        current = ""
        for paragraph in paragraphs:
            if current and len(current) + len(paragraph) + 2 > target_chars:
                chunks.append(Chunk(len(chunks), section.locator, current.strip()))
                tail = ""
                if overlap_chars:
                    overlap_start = max(0, len(current) - overlap_chars)
                    if overlap_start:
                        whitespace = re.search(r"\s", current[overlap_start:])
                        if whitespace:
                            overlap_start += whitespace.end()
                    tail = current[overlap_start:]
                current = f"{tail}\n\n{paragraph}".strip()
            else:
                current = f"{current}\n\n{paragraph}".strip()
        if current:
            chunks.append(Chunk(len(chunks), section.locator, current.strip()))
    return chunks


def readable_title(path: Path) -> str:
    stem = re.sub(r"[_-]+", " ", path.stem)
    stem = re.sub(r"\b[0-9a-f]{8,}\b", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem).strip()
    words = stem.split()[:8]
    return " ".join(word if word.isupper() else word.capitalize() for word in words) or "Untitled Source"
