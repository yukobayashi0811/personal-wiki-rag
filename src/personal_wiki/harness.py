from __future__ import annotations

import re
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .documents import SourceDocument, chunk_document, discover_sources, load_source, readable_title
from .evidence import chat_citations_are_complete, citations_are_valid, save_run
from .model import LocalGemma
from .prompts import INSUFFICIENT_EVIDENCE, ask_messages, chat_system_prompt, wiki_note_messages
from .settings import Settings
from .store import SearchResult, WikiStore


SOURCE_METADATA = {
    "AI Agent Fundamentals": {
        "topic": "Agent Foundations",
        "description": "Definitions, agency levels, reasoning, planning, tools, and actions.",
        "upstream_revision": "b3946b1d09d29c65736e219d48a8a736a2c52154",
    },
    "AI Agents Study Guide": {
        "topic": "Agent System Design",
        "description": "RAG, context, memory, orchestration, observability, and security.",
        "upstream_revision": "25b7985f3b2dc37a84f4a7387ccd3c9f0e5b1595",
    },
    "Evaluating AI Agents": {
        "topic": "Agent Evaluation",
        "description": "Tasks, metrics, verifiers, failure analysis, and production evaluation.",
        "upstream_revision": "d0daf079e7c8da56670886b48c329e9f9fc8281d",
    },
}


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:closing].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def frontmatter(values: dict[str, str | bool]) -> str:
    lines = ["---"]
    for key, value in values.items():
        rendered = str(value).lower() if isinstance(value, bool) else str(value)
        if any(character in rendered for character in (":", "#", "[", "]")):
            rendered = f'"{rendered}"'
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


class PersonalWikiHarness:
    EXPLICIT_RETRIEVAL = (
        re.compile(r"\b(?:my|our) notes\b", re.IGNORECASE),
        re.compile(r"\bthe wiki\b", re.IGNORECASE),
        re.compile(r"\bmy sources\b", re.IGNORECASE),
        re.compile(r"\baccording to\b", re.IGNORECASE),
        re.compile(r"\bcite(?:d|s|ation|ations)?\b", re.IGNORECASE),
    )
    KNOWLEDGE_QUESTION = re.compile(
        r"\b(?:what|how|why|explain|define|compare|difference)\b", re.IGNORECASE
    )
    DOMAIN_TERMS = re.compile(
        r"\b(?:agent|agents|model|swap|pass|context|memory|tool|tools|rag|retrieval|"
        r"evaluation|harness|planning|orchestration|verifier|verifiers)\b",
        re.IGNORECASE,
    )
    META_OR_EDIT = (
        re.compile(r"\bwhat can (?:you|we)\b", re.IGNORECASE),
        re.compile(r"\bhelp me with\b", re.IGNORECASE),
        re.compile(r"\b(?:help me )?draft\b", re.IGNORECASE),
        re.compile(r"\bmake that\b", re.IGNORECASE),
        re.compile(r"\bshorter\b", re.IGNORECASE),
        re.compile(r"\brewrite\b", re.IGNORECASE),
        re.compile(r"\bremember it\b", re.IGNORECASE),
    )
    PROPOSAL_REQUEST = re.compile(
        r"\b(?:draft|plan|idea|ideas|brainstorm|make that|shorter|rewrite)\b",
        re.IGNORECASE,
    )

    def __init__(self, settings: Settings):
        self.settings = settings
        self.settings.ensure_directories()
        self.model = LocalGemma(settings.model_id)

    def _read_instructions(self, path: Path) -> str:
        return path.read_text(encoding="utf-8").strip()

    def search(self, query: str) -> list[SearchResult]:
        with WikiStore(self.settings.database_path) as store:
            return store.search(query, self.settings.top_k)

    @classmethod
    def chat_needs_retrieval(
        cls,
        message: str,
        top_score: float | None = None,
        threshold: float = 2.5,
    ) -> bool:
        stripped = message.strip()
        if stripped.lower().startswith("/notes "):
            return True
        if any(pattern.search(stripped) for pattern in cls.EXPLICIT_RETRIEVAL):
            return True
        if any(pattern.search(stripped) for pattern in cls.META_OR_EDIT):
            return False
        if not cls.KNOWLEDGE_QUESTION.search(stripped):
            return False
        if not cls.DOMAIN_TERMS.search(stripped):
            return False
        return top_score is not None and top_score >= threshold

    def ask(self, question: str, save: bool = True) -> str:
        wall_started = time.perf_counter()
        results = self.search(question)
        if not results:
            answer = INSUFFICIENT_EVIDENCE
            if save:
                save_run(
                    self.settings.evidence_dir,
                    "ask",
                    question,
                    answer,
                    self.settings.model_id,
                    results,
                    wall_seconds=time.perf_counter() - wall_started,
                )
            return answer

        rules = self._read_instructions(self.settings.research_rules_path)
        generated = self.model.generate(
            ask_messages(question, results, rules),
            max_tokens=self.settings.max_tokens,
            temperature=0.1,
        )
        generations = [asdict(generated.metrics)]
        answer = generated.text
        repair_attempted = False
        if answer != INSUFFICIENT_EVIDENCE and not citations_are_valid(answer, len(results)):
            repair_attempted = True
            repair_messages = ask_messages(question, results, rules)
            repair_messages.append({"role": "assistant", "content": answer})
            repair_messages.append(
                {
                    "role": "user",
                    "content": "Rewrite the answer with valid [S#] citations for every material claim.",
                }
            )
            repaired = self.model.generate(
                repair_messages,
                max_tokens=self.settings.max_tokens,
                temperature=0.0,
            )
            generations.append(asdict(repaired.metrics))
            generated = repaired
            answer = repaired.text
            if not citations_are_valid(answer, len(results)):
                answer = INSUFFICIENT_EVIDENCE
        if save:
            save_run(
                self.settings.evidence_dir,
                "ask",
                question,
                answer,
                self.settings.model_id,
                results,
                asdict(generated.metrics),
                repair_attempted=repair_attempted,
                generation_metrics=generations,
                wall_seconds=time.perf_counter() - wall_started,
            )
        return answer

    def chat_turn(
        self,
        message: str,
        history: list[dict[str, str]],
        save: bool = False,
    ) -> str:
        query = message.strip()
        forced_notes = query.lower().startswith("/notes ")
        if forced_notes:
            query = query[7:].strip()

        candidates: list[SearchResult] = []
        forced_or_explicit = self.chat_needs_retrieval(message)
        could_be_knowledge = (
            self.KNOWLEDGE_QUESTION.search(message) is not None
            and not any(pattern.search(message) for pattern in self.META_OR_EDIT)
            and self.DOMAIN_TERMS.search(message) is not None
        )
        if forced_or_explicit or could_be_knowledge:
            candidates = self.search(query)
        top_score = candidates[0].score if candidates else None
        use_retrieval = forced_or_explicit or self.chat_needs_retrieval(
            message,
            top_score=top_score,
            threshold=self.settings.chat_retrieval_threshold,
        )
        results = candidates if use_retrieval else []

        persona = self._read_instructions(self.settings.persona_path)
        rules = self._read_instructions(self.settings.research_rules_path)
        bounded_history = history[-(self.settings.chat_turns * 2) :]
        proposal_request = not results and self.PROPOSAL_REQUEST.search(message) is not None
        model_message = query
        if forced_notes:
            model_message = (
                "Using only the retrieved notes, briefly and directly explain the requested topic. "
                "Prefer two short paragraphs or bullets. End every factual paragraph or bullet "
                "with a valid [S#] citation.\n\n"
                f"Requested topic: {query}"
            )
        elif proposal_request:
            model_message = (
                "Your response must begin with the exact text 'Suggestion:'. "
                "Do not write any characters before it.\n\n"
                f"Original request: {query}"
            )
        messages = [
            {"role": "system", "content": chat_system_prompt(persona, rules, results)},
            *bounded_history,
            {"role": "user", "content": model_message},
        ]
        generated = self.model.generate(
            messages,
            max_tokens=self.settings.max_tokens,
            temperature=0.5,
        )
        generations = [asdict(generated.metrics)]
        answer = generated.text
        repair_attempted = False
        if (
            not results
            and self.PROPOSAL_REQUEST.search(message)
            and not answer.startswith("Suggestion:")
        ):
            repair_attempted = True
            repair_messages = [
                *messages,
                {"role": "assistant", "content": answer},
                {
                    "role": "user",
                    "content": (
                        "Rewrite the response so its first exact characters are 'Suggestion:'. "
                        "Keep the substance concise and do not add factual claims from notes."
                    ),
                },
            ]
            generated = self.model.generate(
                repair_messages,
                max_tokens=self.settings.max_tokens,
                temperature=0.0,
            )
            generations.append(asdict(generated.metrics))
            answer = generated.text
        elif results and not chat_citations_are_complete(answer, len(results)):
            repair_attempted = True
            repair_messages = [
                *messages,
                {"role": "assistant", "content": answer},
                {
                    "role": "user",
                    "content": (
                        "Rewrite the answer using only the supplied evidence. Every factual prose "
                        "paragraph and every factual bullet or numbered item must end with one or "
                        "more valid [S#] citations. Headings need no citation."
                    ),
                },
            ]
            generated = self.model.generate(
                repair_messages,
                max_tokens=self.settings.max_tokens,
                temperature=0.0,
            )
            generations.append(asdict(generated.metrics))
            answer = generated.text
            if not chat_citations_are_complete(answer, len(results)):
                answer = INSUFFICIENT_EVIDENCE
        if save:
            save_run(
                self.settings.evidence_dir,
                "chat",
                message,
                answer,
                self.settings.model_id,
                results,
                asdict(generated.metrics),
                repair_attempted=repair_attempted,
                generation_metrics=generations,
            )
        return answer

    def ingest(self, generate_notes: bool = True) -> dict[str, Any]:
        source_paths = discover_sources(self.settings.raw_dir)
        if len(source_paths) < 3:
            raise RuntimeError(
                "At least three source documents are required in vault/raw before ingestion."
            )
        changed = 0
        chunks_written = 0
        documents: list[SourceDocument] = []
        changed_documents: list[SourceDocument] = []
        current_paths: set[str] = set()
        with WikiStore(self.settings.database_path) as store:
            for path in source_paths:
                document = load_source(path, self.settings.raw_dir)
                current_paths.add(document.relative_path)
                chunks = chunk_document(document)
                if store.upsert_document(document, chunks):
                    changed += 1
                    chunks_written += len(chunks)
                    changed_documents.append(document)
                documents.append(document)
            removed = store.remove_missing_documents(current_paths)

        note_stats = {
            "drafts_written": 0,
            "notes_created": 0,
            "notes_protected": 0,
        }
        truncated_sources = [
            document.relative_path
            for document in documents
            if len("\n\n".join(section.text for section in document.sections)) > 24_000
        ]
        if generate_notes and changed_documents:
            note_stats = self._generate_notes(changed_documents, documents)
        self._write_index()
        return {
            "sources_found": len(source_paths),
            "sources_changed": changed,
            "sources_removed": removed,
            "chunks_written": chunks_written,
            **note_stats,
            "truncated_sources": truncated_sources,
        }

    def _generate_notes(
        self,
        changed_documents: list[SourceDocument],
        all_documents: list[SourceDocument],
    ) -> dict[str, int]:
        summaries_dir = self.settings.wiki_dir / "Source Summaries"
        summaries_dir.mkdir(parents=True, exist_ok=True)
        self.settings.drafts_dir.mkdir(parents=True, exist_ok=True)
        all_titles = [readable_title(document.path) for document in all_documents]
        stats = {"drafts_written": 0, "notes_created": 0, "notes_protected": 0}

        for document in changed_documents:
            title = readable_title(document.path)
            source_text = "\n\n".join(section.text for section in document.sections)
            related = [other for other in all_titles if other != title]
            result = self.model.generate(
                wiki_note_messages(title, document.relative_path, source_text, related),
                max_tokens=1_400,
                temperature=0.2,
            )
            draft_path = self.settings.drafts_dir / f"{title}.md"
            draft_path.write_text(result.text.rstrip() + "\n", encoding="utf-8")
            stats["drafts_written"] += 1

            note_path = summaries_dir / f"{title}.md"
            existed = note_path.exists()
            if existed:
                metadata = read_frontmatter(note_path)
                protected = (
                    not metadata
                    or metadata.get("reviewed", "false").lower() == "true"
                    or metadata.get("ingest_protected", "false").lower() == "true"
                    or metadata.get("origin") not in {"generated", "gemma-draft"}
                )
                if protected:
                    stats["notes_protected"] += 1
                    print(
                        f"Protected existing note: {note_path.relative_to(self.settings.project_root)}; "
                        f"review the new draft at {draft_path.relative_to(self.settings.project_root)}."
                    )
                    continue

            details = SOURCE_METADATA.get(
                title,
                {
                    "topic": "Source Summaries",
                    "description": f"Summary of {document.relative_path}.",
                    "upstream_revision": "unknown",
                },
            )
            note_body = result.text.strip()
            if not note_body.startswith(f"# {title}"):
                note_body = f"# {title}\n\n{note_body}"
            source_link = f"[[raw/{document.relative_path}|Source: {title}]]"
            if source_link not in note_body:
                note_body += f"\n\n## Source\n\n- {source_link}"
            note_text = frontmatter(
                {
                    "reviewed": False,
                    "origin": "generated",
                    "source": f"raw/{document.relative_path}",
                    "source_sha256": document.sha256,
                    "upstream_revision": details["upstream_revision"],
                    "topic": details["topic"],
                    "description": details["description"],
                }
            )
            note_path.write_text(f"{note_text}\n\n{note_body.rstrip()}\n", encoding="utf-8")
            if not existed:
                stats["notes_created"] += 1
        return stats

    def _write_index(self) -> None:
        grouped: dict[str, list[tuple[str, str, str]]] = {}
        for note_path in sorted(self.settings.wiki_dir.rglob("*.md")):
            metadata = read_frontmatter(note_path)
            if not metadata:
                continue
            topic = metadata.get("topic", "Other")
            description = metadata.get("description", "No description provided.")
            title = note_path.stem
            link = note_path.relative_to(self.settings.vault_dir).with_suffix("").as_posix()
            grouped.setdefault(topic, []).append((title, link, description))

        index_lines = [
            "# Personal Wiki",
            "",
            "Start at this index, open a subject note, follow a related-note link, and then open its source link to inspect the unchanged original.",
            "",
        ]
        for topic in sorted(grouped):
            index_lines.extend([f"## {topic}", ""])
            for title, link, description in sorted(grouped[topic]):
                index_lines.append(f"- [[{link}|{title}]] — {description}")
            index_lines.append("")
        (self.settings.vault_dir / "index.md").write_text(
            "\n".join(index_lines).rstrip() + "\n", encoding="utf-8"
        )
