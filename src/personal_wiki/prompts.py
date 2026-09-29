from __future__ import annotations

from .store import SearchResult


INSUFFICIENT_EVIDENCE = "The available sources do not contain enough evidence to answer this question."


def format_evidence(results: list[SearchResult]) -> str:
    blocks = []
    for index, result in enumerate(results, start=1):
        blocks.append(
            f"[S{index}] Source: vault/raw/{result.source_path}; Location: {result.locator}\n"
            f"{result.text}"
        )
    return "\n\n".join(blocks)


def ask_messages(question: str, evidence: list[SearchResult], rules: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                f"{rules}\n\n"
                "Answer in a neutral voice using only the supplied evidence. "
                "Keep the answer concise and directly responsive. "
                "Cite every material factual claim with one or more source markers such as [S1]. "
                f"If the evidence is insufficient, respond exactly: {INSUFFICIENT_EVIDENCE}"
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nEvidence:\n{format_evidence(evidence)}",
        },
    ]


def chat_system_prompt(persona: str, rules: str, evidence: list[SearchResult]) -> str:
    prompt = (
        f"{persona}\n\n"
        "You are operating in chat mode. Use only the bounded recent conversation for follow-ups. "
        "You can brainstorm, draft, plan, compare options, and work through ideas. "
        "When a request needs the local wiki, chat searches the local source index automatically; "
        "the user can force this with /notes <query>. Other commands are wiki ask for a standalone "
        "source-grounded answer, wiki search for original passages, wiki ingest to update the local "
        "index and drafts, and wiki status to inspect local configuration. There is no internet "
        "access and no memory across chat sessions. For a capability question, finish with one "
        "concrete suggested starting point. "
        "Do not claim that you searched notes unless evidence appears below. "
        "Any plan or idea not derived from the notes must begin with 'Suggestion:'. "
        "Never invent personal facts."
    )
    if evidence:
        prompt += (
            f"\n\nWhen making claims from the notes, follow these research rules:\n{rules}\n\n"
            f"Retrieved note evidence:\n{format_evidence(evidence)}"
        )
    return prompt


def wiki_note_messages(
    title: str,
    source_path: str,
    source_text: str,
    related_notes: list[str],
) -> list[dict[str, str]]:
    related = "\n".join(f"- [[wiki/Source Summaries/{name}|{name}]]" for name in related_notes)
    return [
        {
            "role": "system",
            "content": (
                "Create one concise Obsidian note from the supplied source. Return Markdown only. "
                "Output the finished note directly; do not explain your reasoning or review process. "
                "Start with the exact H1 title requested. Include Summary, Key Ideas, Source, and "
                "Related Notes sections. Do not invent facts. Keep all claims traceable to the source. "
                "Use the exact vault-root Source link supplied below. Use only the supplied existing "
                "note links in Related Notes; do not invent a note name."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Required H1 title: {title}\n"
                f"Required Source link: [[raw/{source_path}|Source: {title}]]\n"
                f"Existing related note links:\n{related or '- None'}\n\n"
                f"Source text:\n{source_text[:24_000]}"
            ),
        },
    ]
