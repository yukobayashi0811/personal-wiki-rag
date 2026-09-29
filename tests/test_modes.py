from pathlib import Path

from personal_wiki.evidence import chat_citations_are_complete, citations_are_valid
from personal_wiki.harness import PersonalWikiHarness
from personal_wiki.model import GenerationMetrics, GenerationResult, clean_model_output
from personal_wiki.prompts import chat_system_prompt
from personal_wiki.settings import Settings
from personal_wiki.store import SearchResult


DO_NOT_RETRIEVE = (
    "What can you help me with?",
    "What can we do?",
    "Draft a three-step plan for learning AI agents.",
    "Make that shorter.",
    "Help me draft a design document for my team",
    "My favorite color for this conversation is teal. Please remember it.",
    "What is an open-source license?",
)


def test_chat_does_not_retrieve_for_meta_drafting_or_unrelated_questions() -> None:
    for message in DO_NOT_RETRIEVE:
        assert PersonalWikiHarness.chat_needs_retrieval(message, top_score=100.0) is False


def test_chat_retrieves_when_notes_are_explicitly_requested() -> None:
    assert PersonalWikiHarness.chat_needs_retrieval("According to my notes, what are tools?") is True
    assert PersonalWikiHarness.chat_needs_retrieval("/notes context and memory") is True


def test_chat_retrieves_for_high_scoring_domain_questions() -> None:
    assert PersonalWikiHarness.chat_needs_retrieval(
        "Explain the model swap experiment.", top_score=5.9
    ) is True
    assert PersonalWikiHarness.chat_needs_retrieval("What is pass^k?", top_score=2.7) is True
    assert PersonalWikiHarness.chat_needs_retrieval(
        "Explain the model swap experiment.", top_score=2.4
    ) is False


def test_citation_validation_rejects_missing_and_unknown_sources() -> None:
    assert citations_are_valid("The claim is supported [S1].", 2) is True
    assert citations_are_valid("The claim has no citation.", 2) is False
    assert citations_are_valid("The claim cites an unknown source [S3].", 2) is False


def test_chat_citation_validation_requires_every_material_line() -> None:
    complete = "Definition is supported by the source passage [S1].\n\n- Another material claim is supported here [S2]."
    incomplete = "Definition is supported by the source passage.\n\n- Another material claim is supported here [S2]."
    assert chat_citations_are_complete(complete, 2) is True
    assert chat_citations_are_complete(incomplete, 2) is False


def test_model_output_keeps_only_final_channel() -> None:
    raw = "private reasoning<channel|># Final Answer\n\nVisible text.<turn|>"
    assert clean_model_output(raw) == "# Final Answer\n\nVisible text."


def test_chat_prompt_declares_real_capabilities_and_suggestion_rule() -> None:
    prompt = chat_system_prompt("Persona", "Rules", [])
    for required in (
        "/notes <query>",
        "wiki ask",
        "wiki search",
        "wiki ingest",
        "wiki status",
        "no internet",
        "no memory across",
        "Suggestion:",
    ):
        assert required in prompt


def test_chat_repairs_a_proposal_that_does_not_start_with_suggestion(tmp_path: Path) -> None:
    settings = Settings.from_environment(tmp_path)
    settings.persona_path.parent.mkdir(parents=True, exist_ok=True)
    settings.persona_path.write_text("Persona", encoding="utf-8")
    settings.research_rules_path.write_text("Rules", encoding="utf-8")
    harness = PersonalWikiHarness(settings)

    class FakeModel:
        def __init__(self) -> None:
            self.calls = 0

        def generate(self, *_args, **kwargs) -> GenerationResult:
            self.calls += 1
            text = "Suggestion: Draft body."
            return GenerationResult(text, GenerationMetrics(0.1, 1.0, 1.0, None))

    model = FakeModel()
    harness.model = model
    answer = harness.chat_turn("Help me draft a design document for my team", [], save=False)
    assert answer == "Suggestion: Draft body."
    assert model.calls == 1


def test_notes_command_forces_a_concise_cited_request(tmp_path: Path) -> None:
    settings = Settings.from_environment(tmp_path)
    settings.persona_path.parent.mkdir(parents=True, exist_ok=True)
    settings.persona_path.write_text("Persona", encoding="utf-8")
    settings.research_rules_path.write_text("Rules", encoding="utf-8")
    harness = PersonalWikiHarness(settings)
    harness.search = lambda _query: [SearchResult("source.md", "Context", "Evidence", 3.0)]

    class FakeModel:
        messages = []

        def generate(self, messages, **_kwargs) -> GenerationResult:
            self.messages = messages
            return GenerationResult(
                "Context is information supplied to the current model call [S1].",
                GenerationMetrics(0.1, 1.0, 1.0, None),
            )

    model = FakeModel()
    harness.model = model
    answer = harness.chat_turn("/notes context and memory", [], save=False)
    assert answer.endswith("[S1].")
    assert "briefly and directly explain" in model.messages[-1]["content"]
