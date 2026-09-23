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
        "You are operating in chat mode. Use recent conversation for follow-ups. "
        "Help with brainstorming, drafting, planning, and working through ideas. "
        "Do not claim that you searched notes unless evidence appears below. "
        "Label proposals as suggestions and never invent personal facts."
    )
    if evidence:
        prompt += (
            f"\n\nWhen making claims from the notes, follow these research rules:\n{rules}\n\n"
            f"Retrieved note evidence:\n{format_evidence(evidence)}"
        )
    return prompt


def wiki_note_messages(title: str, source_path: str, source_text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "Create one concise Obsidian note from the supplied source. Return Markdown only. "
                "Start with the exact H1 title requested. Include Summary, Key Ideas, Source, and "
                "Related Notes sections. Do not invent facts. Keep all claims traceable to the source."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Required H1 title: {title}\nSource path: vault/raw/{source_path}\n\n"
                f"Source text:\n{source_text[:24_000]}"
            ),
        },
    ]

