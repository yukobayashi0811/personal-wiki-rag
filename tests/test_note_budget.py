from pathlib import Path

import pytest

from personal_wiki.documents import SourceDocument, SourceSection
from personal_wiki.harness import PersonalWikiHarness
from personal_wiki.settings import Settings


class CharacterTokenizer:
    @staticmethod
    def encode(text, add_special_tokens=False):
        del add_special_tokens
        return list(text)

    @staticmethod
    def decode(tokens, skip_special_tokens=True):
        del skip_special_tokens
        return "".join(tokens)

    @staticmethod
    def apply_chat_template(messages, tokenize=False, add_generation_prompt=True):
        del tokenize, add_generation_prompt
        return "\n".join(message["content"] for message in messages)


class RecordingModel:
    def __init__(self):
        self._tokenizer = CharacterTokenizer()
        self.messages = None
        self.max_tokens = None

    def load(self):
        return None

    def generate(self, messages, max_tokens, **_kwargs):
        self.messages = messages
        self.max_tokens = max_tokens
        return type("Result", (), {"text": "# Example\n\nGenerated body."})()


def _document(tmp_path: Path, text: str) -> SourceDocument:
    path = tmp_path / "vault" / "raw" / "Example.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return SourceDocument(
        path=path,
        relative_path="Example.md",
        sha256="example",
        sections=(SourceSection("Example", text),),
    )


def test_note_source_is_truncated_on_token_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("WIKI_NOTE_SOURCE_MAX_TOKENS", "5")
    monkeypatch.setenv("WIKI_NOTE_MAX_TOKENS", "77")
    settings = Settings.from_environment(tmp_path)
    harness = PersonalWikiHarness(settings)
    model = RecordingModel()
    harness.model = model
    doc = _document(tmp_path, "abcdefghij")

    stats = harness._generate_notes([doc], [doc])

    assert stats["source_token_counts"] == {"Example.md": 10}
    assert stats["truncated_sources"] == ["Example.md"]
    assert model.messages[-1]["content"].endswith("Source text:\nabcde")
    assert model.max_tokens == 77


def test_note_source_is_not_truncated_when_it_fits(tmp_path: Path) -> None:
    settings = Settings.from_environment(tmp_path)
    harness = PersonalWikiHarness(settings)
    model = RecordingModel()
    harness.model = model
    doc = _document(tmp_path, "complete source")

    stats = harness._generate_notes([doc], [doc])

    assert stats["source_token_counts"] == {"Example.md": 15}
    assert stats["truncated_sources"] == []
    assert model.messages[-1]["content"].endswith("Source text:\ncomplete source")


@pytest.mark.parametrize(
    "name",
    ("WIKI_NOTE_SOURCE_MAX_TOKENS", "WIKI_NOTE_MAX_TOKENS"),
)
def test_note_token_settings_must_be_positive(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.setenv(name, "0")
    with pytest.raises(ValueError, match=f"{name} must be a positive integer"):
        Settings.from_environment(tmp_path)
