from infra.hubspot.notes import HubspotNotes
from tests.mocks.mock_hubspot_api import MockHubspotApi

mock_hubspot_api = MockHubspotApi()
hubspot_notes = HubspotNotes()


def test_create_hubspot_note_associated_to_contact_success(monkeypatch):
    def fake_post(*args, **kwargs):
        return mock_hubspot_api.return_a_created_object()
    monkeypatch.setattr("infra.hubspot.notes.requests.post", fake_post)
    note_id = hubspot_notes.create_hubspot_note_associated_to_contact(
        note_text="Test note",
        contact_id="123"
    )
    assert note_id == "1"
    