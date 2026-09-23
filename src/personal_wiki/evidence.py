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
) -> tuple[Path, Path]:
    runs_dir = evidence_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC)
    # Microseconds prevent evidence from being overwritten when several chat
    # turns finish within the same second.
    stem = f"{timestamp.strftime('%Y%m%dT%H%M%S%fZ')}-{mode}"
    payload = {
        "timestamp_utc": timestamp.isoformat(),
        "mode": mode,
        "execution": "local",
        "model": model_id,
        "input": input_text,
        "retrieved_passages": [asdict(result) for result in results],
        "output": output_text,
        "metrics": metrics or {},
    }
    json_path = runs_dir / f"{stem}.json"
    markdown_path = runs_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    passages = "\n\n".join(
        f"### S{index}: `{result.source_path}` ({result.locator})\n\n{result.text}"
        for index, result in enumerate(results, start=1)
    ) or "No passages were retrieved."
    markdown_path.write_text(
        f"# {mode.title()} Evidence\n\n"
        f"- Timestamp (UTC): `{timestamp.isoformat()}`\n"
        f"- Execution: `local`\n"
        f"- Model: `{model_id or 'not used'}`\n\n"
        f"## Input\n\n{input_text}\n\n"
        f"## Retrieved Passages\n\n{passages}\n\n"
        f"## Actual Output\n\n{output_text}\n",
        encoding="utf-8",
    )
    return json_path, markdown_path
