from pathlib import Path
from types import SimpleNamespace

from personal_wiki.documents import SourceDocument, SourceSection
from personal_wiki.harness import PersonalWikiHarness
from personal_wiki.settings import Settings


class FakeModel:
    def generate(self, *_args, **_kwargs):
        return SimpleNamespace(text="# Example\n\nGenerated body.")


def document(tmp_path: Path) -> SourceDocument:
    source = tmp_path / "vault" / "raw" / "Example.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("source", encoding="utf-8")
    return SourceDocument(
        path=source,
        relative_path="Example.md",
        sha256="abc123",
        sections=(SourceSection("Example", "source text"),),
    )


def test_note_generation_writes_draft_but_protects_existing_note(tmp_path: Path) -> None:
    settings = Settings.from_environment(tmp_path)
    harness = PersonalWikiHarness(settings)
    harness.model = FakeModel()
    doc = document(tmp_path)
    note = settings.wiki_dir / "Source Summaries" / "Example.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    original = "---\nreviewed: true\n---\n\n# Example\n\nHuman text.\n"
    note.write_text(original, encoding="utf-8")

    stats = harness._generate_notes([doc], [doc])

    assert stats == {"drafts_written": 1, "notes_created": 0, "notes_protected": 1}
    assert note.read_text(encoding="utf-8") == original
    assert (settings.drafts_dir / "Example.md").read_text(encoding="utf-8") == (
        "# Example\n\nGenerated body.\n"
    )


def test_unreviewed_generated_note_updates_in_place_without_duplicate(tmp_path: Path) -> None:
    settings = Settings.from_environment(tmp_path)
    harness = PersonalWikiHarness(settings)
    harness.model = FakeModel()
    doc = document(tmp_path)
    note = settings.wiki_dir / "Source Summaries" / "Example.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\nreviewed: false\norigin: generated\n---\n\n# Example\n\nOld text.\n",
        encoding="utf-8",
    )

    stats = harness._generate_notes([doc], [doc])

    assert stats == {"drafts_written": 1, "notes_created": 0, "notes_protected": 0}
    assert len(list(note.parent.glob("Example*.md"))) == 1
    assert "Generated body." in note.read_text(encoding="utf-8")
