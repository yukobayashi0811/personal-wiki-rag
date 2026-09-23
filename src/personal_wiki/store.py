from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .documents import Chunk, SourceDocument


@dataclass(frozen=True)
class SearchResult:
    source_path: str
    locator: str
    text: str
    score: float


class WikiStore:
    def __init__(self, database_path: Path):
        database_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "WikiStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                source_path TEXT NOT NULL UNIQUE,
                sha256 TEXT NOT NULL,
                indexed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                chunk_index INTEGER NOT NULL,
                source_path TEXT NOT NULL,
                locator TEXT NOT NULL,
                text TEXT NOT NULL,
                UNIQUE(document_id, chunk_index)
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                text,
                content='chunks',
                content_rowid='id',
                tokenize='porter unicode61'
            );
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
            END;
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, text)
                VALUES ('delete', old.id, old.text);
            END;
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, text)
                VALUES ('delete', old.id, old.text);
                INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
            END;
            """
        )

    def upsert_document(self, document: SourceDocument, chunks: list[Chunk]) -> bool:
        existing = self.connection.execute(
            "SELECT id, sha256 FROM documents WHERE source_path = ?",
            (document.relative_path,),
        ).fetchone()
        if existing and existing["sha256"] == document.sha256:
            return False
        with self.connection:
            if existing:
                document_id = int(existing["id"])
                self.connection.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
                self.connection.execute(
                    "UPDATE documents SET sha256 = ?, indexed_at = ? WHERE id = ?",
                    (document.sha256, datetime.now(UTC).isoformat(), document_id),
                )
            else:
                cursor = self.connection.execute(
                    "INSERT INTO documents(source_path, sha256, indexed_at) VALUES (?, ?, ?)",
                    (document.relative_path, document.sha256, datetime.now(UTC).isoformat()),
                )
                document_id = int(cursor.lastrowid)
            self.connection.executemany(
                """
                INSERT INTO chunks(document_id, chunk_index, source_path, locator, text)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (document_id, chunk.index, document.relative_path, chunk.locator, chunk.text)
                    for chunk in chunks
                ],
            )
        return True

    @staticmethod
    def _fts_query(query: str) -> str:
        stop_words = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
            "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
            "what", "when", "where", "which", "who", "why", "with", "can", "could",
            "do", "does", "did", "defined", "difference", "team",
        }
        terms = [
            token.lower()
            for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.-]*", query)
            if token.lower() not in stop_words and len(token) > 1
        ]
        if not terms:
            terms = re.findall(r"[A-Za-z0-9]+", query)
        return " OR ".join(f'"{term.replace(chr(34), chr(34) * 2)}"*' for term in terms[:12])

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        fts_query = self._fts_query(query)
        if not fts_query:
            return []
        rows = self.connection.execute(
            """
            SELECT c.source_path, c.locator, c.text, bm25(chunks_fts) AS rank
            FROM chunks_fts
            JOIN chunks AS c ON c.id = chunks_fts.rowid
            WHERE chunks_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()
        return [
            SearchResult(
                source_path=row["source_path"],
                locator=row["locator"],
                text=row["text"],
                score=float(-row["rank"]),
            )
            for row in rows
        ]

    def document_count(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0])

    def chunk_count(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])
