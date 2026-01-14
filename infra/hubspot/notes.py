import requests
import time
from infra.hubspot.general import (
    HUBSPOT_CRM_API_BASE_URL, 
    HUBSPOT_CRM_API_HEADERS,
    HUBSPOT_INTEGRATION_OWNER_ID,
    HUBSPOT_ASSOCIATION_TYPE_NOTE_TO_CONTACT
)

class HubspotNotes:

    HUBSPOT_API_NOTES_URL = f'{HUBSPOT_CRM_API_BASE_URL}notes/'

    def create_hubspot_note_associated_to_contact(self, note_text:str, id_contact:str):
        now_timestamp = int(time.time()*1000)
        payload = {
            'properties': {
                'hs_timestamp': now_timestamp,
                'hs_note_body': note_text,
                'hubspot_owner_id': HUBSPOT_INTEGRATION_OWNER_ID,
            },
            'associations': [
                {
                    'to': {
                        'id': id_contact
                    },
                    'types': [
                        {
                        'associationCategory': 'HUBSPOT_DEFINED',
                        'associationTypeId': HUBSPOT_ASSOCIATION_TYPE_NOTE_TO_CONTACT
                        }
                    ]
                }
            ]
        }
        response = requests.post(self.HUBSPOT_API_NOTES_URL, json=payload, headers=HUBSPOT_CRM_API_HEADERS)
        response.raise_for_status()
        return response.json()['id']
    