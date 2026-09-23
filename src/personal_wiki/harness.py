from __future__ import annotations

import re
from dataclasses import asdict
from pathlib import Path

from .documents import chunk_document, discover_sources, load_source, readable_title
from .evidence import citations_are_valid, save_run
from .model import LocalGemma
from .prompts import INSUFFICIENT_EVIDENCE, ask_messages, chat_system_prompt, wiki_note_messages
from .settings import Settings
from .store import SearchResult, WikiStore


class PersonalWikiHarness:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.settings.ensure_directories()
        self.model = LocalGemma(settings.model_id)

    def _read_instructions(self, path: Path) -> str:
        return path.read_text(encoding="utf-8").strip()

    def search(self, query: str) -> list[SearchResult]:
        with WikiStore(self.settings.database_path) as store:
            return store.search(query, self.settings.top_k)

    @staticmethod
    def chat_needs_retrieval(message: str) -> bool:
        normalized = message.lower()
        explicit = (
            "my notes", "my wiki", "the wiki", "our notes", "source", "document",
            "according to", "from the notes", "cite", "citation",
        )
        return any(phrase in normalized for phrase in explicit)

    def ask(self, question: str, save: bool = True) -> str:
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
                )
            return answer

        rules = self._read_instructions(self.settings.research_rules_path)
        generated = self.model.generate(
            ask_messages(question, results, rules),
            max_tokens=self.settings.max_tokens,
            temperature=0.1,
        )
        answer = generated.text
        if answer != INSUFFICIENT_EVIDENCE and not citations_are_valid(answer, len(results)):
            repair_messages = ask_messages(question, results, rules)
            repair_messages.append({"role": "assistant", "content": answer})
            repair_messages.append(
                {
                    "role": "user",
                    "content": "Rewrite the answer with valid [S#] citations for every material claim.",
                }
            )
            answer = self.model.generate(
                repair_messages,
                max_tokens=self.settings.max_tokens,
                temperature=0.0,
            ).text
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
            )
        return answer

    def chat_turn(
        self,
        message: str,
        history: list[dict[str, str]],
        save: bool = False,
    ) -> str:
        results = self.search(message) if self.chat_needs_retrieval(message) else []
        persona = self._read_instructions(self.settings.persona_path)
        rules = self._read_instructions(self.settings.research_rules_path)
        messages = [
            {"role": "system", "content": chat_system_prompt(persona, rules, results)},
            *history,
            {"role": "user", "content": message},
        ]
        generated = self.model.generate(messages, max_tokens=self.settings.max_tokens, temperature=0.5)
        if save:
            save_run(
                self.settings.evidence_dir,
                "chat",
                message,
                generated.text,
                self.settings.model_id,
                results,
                asdict(generated.metrics),
            )
        return generated.text

    def ingest(self, generate_notes: bool = True) -> dict[str, int]:
        source_paths = discover_sources(self.settings.raw_dir)
        if len(source_paths) < 3:
            raise RuntimeError(
                "At least three source documents are required in vault/raw before ingestion."
            )
        changed = 0
        chunks_written = 0
        documents = []
        changed_documents = []
        with WikiStore(self.settings.database_path) as store:
            for path in source_paths:
                document = load_source(path, self.settings.raw_dir)
                chunks = chunk_document(document)
                if store.upsert_document(document, chunks):
                    changed += 1
                    chunks_written += len(chunks)
                    changed_documents.append(document)
                documents.append(document)

        if generate_notes and changed_documents:
            self._generate_notes(changed_documents)
        self._write_index(documents)
        return {
            "sources_found": len(source_paths),
            "sources_changed": changed,
            "chunks_written": chunks_written,
        }

    def _generate_notes(self, documents: list) -> None:
        concepts_dir = self.settings.wiki_dir / "Concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        for document in documents:
            title = readable_title(document.path)
            source_text = "\n\n".join(section.text for section in document.sections)
            result = self.model.generate(
                wiki_note_messages(title, document.relative_path, source_text),
                max_tokens=1_400,
                temperature=0.2,
            )
            note_path = concepts_dir / f"{title}.md"
            note = result.text.strip()
            if not note.startswith(f"# {title}"):
                note = f"# {title}\n\n{note}"
            if f"vault/raw/{document.relative_path}" not in note:
                note += f"\n\n## Source\n\n- [[../../raw/{document.relative_path}|{document.relative_path}]]\n"
            note_path.write_text(note.rstrip() + "\n", encoding="utf-8")

    def _write_index(self, documents: list) -> None:
        index_lines = ["# Personal Wiki", "", "## Concepts", ""]
        descriptions = {
            "AI Agent Fundamentals": "Definitions, agency levels, reasoning, planning, tools, and actions.",
            "AI Agents Study Guide": "RAG, context, memory, orchestration, observability, and security.",
            "Evaluating AI Agents": "Tasks, metrics, verifiers, failure analysis, and production evaluation.",
        }
        for document in documents:
            title = readable_title(document.path)
            description = descriptions.get(title, f"Reviewed from `{document.relative_path}`.")
            index_lines.append(f"- [[wiki/Concepts/{title}|{title}]] — {description}")
        (self.settings.vault_dir / "index.md").write_text(
            "\n".join(index_lines).rstrip() + "\n", encoding="utf-8"
        )
