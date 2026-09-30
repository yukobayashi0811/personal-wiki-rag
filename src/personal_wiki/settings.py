from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MODEL = "mlx-community/gemma-4-e4b-it-4bit"
DEFAULT_NOTE_SOURCE_MAX_TOKENS = 30_000
DEFAULT_NOTE_MAX_TOKENS = 2_400


def _positive_int_environment(name: str, default: int) -> int:
    value = int(os.getenv(name, str(default)))
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer.")
    return value


@dataclass(frozen=True)
class Settings:
    project_root: Path
    vault_dir: Path
    raw_dir: Path
    wiki_dir: Path
    data_dir: Path
    drafts_dir: Path
    evidence_dir: Path
    database_path: Path
    persona_path: Path
    research_rules_path: Path
    model_id: str
    max_tokens: int
    note_source_max_tokens: int
    note_max_tokens: int
    top_k: int
    chat_turns: int
    chat_retrieval_threshold: float

    @classmethod
    def from_environment(cls, project_root: Path | None = None) -> "Settings":
        root = (project_root or Path.cwd()).resolve()
        vault = root / "vault"
        data = root / "data"
        return cls(
            project_root=root,
            vault_dir=vault,
            raw_dir=vault / "raw",
            wiki_dir=vault / "wiki",
            data_dir=data,
            drafts_dir=data / "drafts",
            evidence_dir=root / "evidence",
            database_path=data / "wiki.db",
            persona_path=root / "config" / "persona.md",
            research_rules_path=root / "config" / "wiki-instructions.md",
            model_id=os.getenv("WIKI_MODEL", DEFAULT_MODEL),
            # Gemma may use part of the generation budget for internal thought
            # before emitting its final channel. This budget avoids truncating
            # a short, source-backed answer on questions that require comparison.
            max_tokens=int(os.getenv("WIKI_MAX_TOKENS", "1400")),
            note_source_max_tokens=_positive_int_environment(
                "WIKI_NOTE_SOURCE_MAX_TOKENS", DEFAULT_NOTE_SOURCE_MAX_TOKENS
            ),
            note_max_tokens=_positive_int_environment(
                "WIKI_NOTE_MAX_TOKENS", DEFAULT_NOTE_MAX_TOKENS
            ),
            top_k=int(os.getenv("WIKI_TOP_K", "5")),
            chat_turns=int(os.getenv("WIKI_CHAT_TURNS", "12")),
            chat_retrieval_threshold=float(os.getenv("WIKI_CHAT_RETRIEVAL_THRESHOLD", "2.5")),
        )

    def ensure_directories(self) -> None:
        for path in (
            self.raw_dir,
            self.wiki_dir,
            self.data_dir,
            self.drafts_dir,
            self.evidence_dir / "runs",
            self.evidence_dir / "screenshots",
            self.evidence_dir / "recordings",
        ):
            path.mkdir(parents=True, exist_ok=True)
