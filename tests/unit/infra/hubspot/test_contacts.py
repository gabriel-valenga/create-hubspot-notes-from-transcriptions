import pytest
from infra.hubspot.contacts import HubspotContacts
from tests.mocks.mock_hubspot_api import MockHubspotApi

mock_hubspot_api = MockHubspotApi()
hubspot_contacts = HubspotContacts()

@pytest.fixture
def mock_hubspot_api_contacts_get_success(monkeypatch):
    def fake_get(*args, **kwargs):
        return mock_hubspot_api.return_an_object_with_success()
    monkeypatch.setattr("infra.hubspot.contacts.requests.get", fake_get)


@pytest.fixture
def mock_hubspot_api_contacts_post_created(monkeypatch):
    def fake_post(*args, **kwargs):
        return mock_hubspot_api.return_a_created_object()
    monkeypatch.setattr("infra.hubspot.contacts.requests.post", fake_post)


@pytest.mark.unit
def test_get_a_contact_by_email_success(mock_hubspot_api_contacts_get_success):    
    contact_id = hubspot_contacts.get_a_contact_id_by_email(email='test@email.com')
    assert contact_id == '1'


@pytest.mark.unit
def test_create_hubspot_contact(mock_hubspot_api_contacts_post_created):
    contact_id = hubspot_contacts.create_hubspot_contact(email='testnew@email.com')
    assert contact_id == '1'
