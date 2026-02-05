import pytest
from business.create_hubspot_notes_from_transcriptions import CreateHubspotNoteFromTranscriptionService
from tests.fakes.business.hubspot.notes import FakeHubspotNotes
from tests.mocks.mock_ai_text_summarizer import MockTextSummarizer


@pytest.mark.integration
def test_create_hubspot_note_from_transcription(monkeypatch):
    mock_text_summarizer = MockTextSummarizer()
    fake_hubspot_notes = FakeHubspotNotes()
    monkeypatch.setattr(
        "business.create_hubspot_notes_from_transcriptions.TextSummarizerService",
        lambda *_: mock_text_summarizer
    )
    monkeypatch.setattr(
        "business.create_hubspot_notes_from_transcriptions.GeminiTextSummarizer",
        lambda *_: None
    )
    monkeypatch.setattr(
        "business.create_hubspot_notes_from_transcriptions.HubspotNotes",
        lambda *_: fake_hubspot_notes
    )
    CreateHubspotNoteFromTranscriptionService().create_hubspot_note_from_transcription(
        transcription='test transcription',
        email='email@test.com'
    )
    assert fake_hubspot_notes.called is True
    assert fake_hubspot_notes.note_text == 'text summary from mock'
    assert fake_hubspot_notes.email == 'email@test.com'
