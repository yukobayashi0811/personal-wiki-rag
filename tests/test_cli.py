import builtins
from pathlib import Path

import pytest

from personal_wiki.cli import build_parser, main
from personal_wiki.model import LocalGemma


@pytest.mark.parametrize("command", [("search", "tools"), ("ask", "What are tools?"), ("chat",)])
def test_empty_index_gives_actionable_error(
    tmp_path: Path, command: tuple[str, ...], capsys: pytest.CaptureFixture[str]
) -> None:
    result = main(["--project-root", str(tmp_path), *command])
    assert result == 2
    assert "The index is empty. Run `wiki ingest` first." in capsys.readouterr().err


def test_missing_mlx_has_friendly_error(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def blocked_import(name: str, *args, **kwargs):
        if name == "mlx_lm" or name.startswith("mlx_lm."):
            raise ImportError("blocked for test")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    with pytest.raises(RuntimeError, match="MLX-LM is missing or this platform is unsupported"):
        LocalGemma("example/model").load()


def test_help_documents_prerequisites_variables_and_examples() -> None:
    help_text = build_parser().format_help()
    assert "Apple Silicon" in help_text
    assert "WIKI_CHAT_TURNS" in help_text
    assert "HF_HUB_OFFLINE" in help_text
    assert "wiki ingest" in help_text
