from personal_wiki.evidence import citations_are_valid
from personal_wiki.harness import PersonalWikiHarness
from personal_wiki.model import clean_model_output


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


def test_model_output_keeps_only_final_channel() -> None:
    raw = "private reasoning<channel|># Final Answer\n\nVisible text.<turn|>"
    assert clean_model_output(raw) == "# Final Answer\n\nVisible text."
