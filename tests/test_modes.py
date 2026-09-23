from personal_wiki.evidence import citations_are_valid
from personal_wiki.harness import PersonalWikiHarness
from personal_wiki.model import clean_model_output


def test_chat_does_not_retrieve_for_capability_question() -> None:
    assert PersonalWikiHarness.chat_needs_retrieval("What can you help me with?") is False


def test_chat_retrieves_when_notes_are_explicitly_requested() -> None:
    assert PersonalWikiHarness.chat_needs_retrieval("What do my notes say about retrieval?") is True


def test_citation_validation_rejects_missing_and_unknown_sources() -> None:
    assert citations_are_valid("The claim is supported [S1].", 2) is True
    assert citations_are_valid("The claim has no citation.", 2) is False
    assert citations_are_valid("The claim cites an unknown source [S3].", 2) is False


def test_model_output_keeps_only_final_channel() -> None:
    raw = "private reasoning<channel|># Final Answer\n\nVisible text.<turn|>"
    assert clean_model_output(raw) == "# Final Answer\n\nVisible text."
