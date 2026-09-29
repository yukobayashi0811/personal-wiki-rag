from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .store import SearchResult


def cited_source_numbers(text: str) -> set[int]:
    return {int(value) for value in re.findall(r"\[S(\d+)\]", text)}


def citations_are_valid(text: str, source_count: int) -> bool:
    cited = cited_source_numbers(text)
    return bool(cited) and all(1 <= number <= source_count for number in cited)


def save_run(
    evidence_dir: Path,
    mode: str,
    input_text: str,
    output_text: str,
    model_id: str | None,
    results: list[SearchResult],
    metrics: dict[str, Any] | None = None,
    *,
    repair_attempted: bool = False,
    generation_metrics: list[dict[str, Any]] | None = None,
    wall_seconds: float | None = None,
) -> tuple[Path, Path]:
    runs_dir = evidence_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC)
    # Microseconds prevent evidence from being overwritten when several chat
    # turns finish within the same second.
    stem = f"{timestamp.strftime('%Y%m%dT%H%M%S%fZ')}-{mode}"
    cited_numbers = sorted(cited_source_numbers(output_text))
    citation_valid = (
        output_text.strip() == "The available sources do not contain enough evidence to answer this question."
        or citations_are_valid(output_text, len(results))
    )
    combined_metrics = dict(metrics or {})
    if wall_seconds is not None:
        combined_metrics["wall_seconds"] = wall_seconds
    if generation_metrics is not None:
        combined_metrics["generations"] = generation_metrics
    payload = {
        "timestamp_utc": timestamp.isoformat(),
        "mode": mode,
        "execution": "local",
        "model": model_id,
        "input": input_text,
        "retrieved_passages": [asdict(result) for result in results],
        "output": output_text,
        "repair_attempted": repair_attempted,
        "cited_sources": [f"S{number}" for number in cited_numbers],
        "citations_valid": citation_valid,
        "metrics": combined_metrics,
    }
    json_path = runs_dir / f"{stem}.json"
    markdown_path = runs_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    passages = "\n\n".join(
        f"### S{index}: `{result.source_path}` ({result.locator})\n\n{result.text}"
        for index, result in enumerate(results, start=1)
    ) or "No passages were retrieved."
    citation_rows = []
    for number in cited_numbers:
        if 1 <= number <= len(results):
            result = results[number - 1]
            citation_rows.append(
                f"- S{number}: `{result.source_path}` — {result.locator}"
            )
    citation_details = "\n".join(citation_rows) or "No source markers were cited."
    markdown_path.write_text(
        f"# {mode.title()} Evidence\n\n"
        f"- Timestamp (UTC): `{timestamp.isoformat()}`\n"
        f"- Execution: `local`\n"
        f"- Model: `{model_id or 'not used'}`\n\n"
        f"- Repair attempted: `{str(repair_attempted).lower()}`\n"
        f"- Citations valid: `{str(citation_valid).lower()}`\n\n"
        f"## Input\n\n{input_text}\n\n"
        f"## Retrieved Passages\n\n{passages}\n\n"
        f"## Actual Output\n\n{output_text}\n\n"
        f"## Citation Check\n\n{citation_details}\n",
        encoding="utf-8",
    )
    return json_path, markdown_path
