import re
from pathlib import Path


def test_all_authored_vault_wikilinks_resolve_exactly_once() -> None:
    vault = Path(__file__).parents[1] / "vault"
    authored = [vault / "index.md", *sorted((vault / "wiki").rglob("*.md"))]
    all_markdown = list(vault.rglob("*.md"))
    failures: list[str] = []

    for note in authored:
        for raw_target in re.findall(r"\[\[([^\]]+)\]\]", note.read_text(encoding="utf-8")):
            target = raw_target.split("|", 1)[0].split("#", 1)[0]
            if not target:
                continue
            candidate = vault / target
            matches = []
            if candidate.suffix:
                if candidate.exists():
                    matches.append(candidate)
            else:
                direct = candidate.with_suffix(".md")
                if direct.exists():
                    matches.append(direct)
                matches.extend(path for path in all_markdown if path.stem == target)
                matches = list(dict.fromkeys(matches))
            if len(matches) != 1:
                failures.append(f"{note.relative_to(vault)} -> {raw_target}: {len(matches)} matches")

    assert not failures, "\n".join(failures)
