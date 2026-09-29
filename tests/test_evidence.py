import json
from pathlib import Path

from personal_wiki.evidence import save_run
from personal_wiki.store import SearchResult


def test_ask_evidence_records_repair_citations_and_wall_time(tmp_path: Path) -> None:
    result = SearchResult("source.md", "Section", "Evidence text.", 1.0)
    json_path, markdown_path = save_run(
        tmp_path,
        "ask",
        "Question?",
        "Supported claim [S1].",
        "model",
        [result],
        {"elapsed_seconds": 1.0},
        repair_attempted=True,
        generation_metrics=[{"elapsed_seconds": 0.5}, {"elapsed_seconds": 1.0}],
        wall_seconds=2.0,
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["repair_attempted"] is True
    assert payload["cited_sources"] == ["S1"]
    assert payload["citations_valid"] is True
    assert payload["metrics"]["wall_seconds"] == 2.0
    assert len(payload["metrics"]["generations"]) == 2
    assert "S1: `source.md` — Section" in markdown_path.read_text(encoding="utf-8")
