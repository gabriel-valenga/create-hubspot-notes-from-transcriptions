import requests
from infra.hubspot.general import HUBSPOT_CRM_API_BASE_URL, HUBSPOT_CRM_API_HEADERS

class HubspotContacts:

    HUBSPOT_API_CONTACTS_URL = f'{HUBSPOT_CRM_API_BASE_URL}contacts/'

    def get_a_contact_id_by_email(self, email:str):
        url = f'{self.HUBSPOT_API_CONTACTS_URL}{email}?idProperty=email'
        response = requests.get(url, headers=HUBSPOT_CRM_API_HEADERS)
        response.raise_for_status()
        contact_id = response.json()['id']
        return contact_id
    

    def create_hubspot_contact(self, email:str):
        payload = {
            'properties':{
                'email': email
            }
        }
        response = requests.post(
            self.HUBSPOT_API_CONTACTS_URL, json=payload, headers=HUBSPOT_CRM_API_HEADERS
        )
        response.raise_for_status()
        return response.json()['id']
