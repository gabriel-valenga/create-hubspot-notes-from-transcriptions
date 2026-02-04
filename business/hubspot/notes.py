import logging
from fastapi import HTTPException
from http import HTTPStatus
from requests import HTTPError
from infra.hubspot.contacts import HubspotContacts
from infra.hubspot.notes import HubspotNotes as InfraHubspotNotes

class HubspotNotes():

    @staticmethod
    def create_hubspot_note_associated_with_a_contact_by_email(note_text:str, email:str):
        try:
            hubspot_contacts = HubspotContacts()
            hubspot_notes = InfraHubspotNotes()
            try:
                contact_id = hubspot_contacts.get_a_contact_id_by_email(email=email)
            except HTTPError as e:
                if e.response.status_code == HTTPStatus.NOT_FOUND:
                    contact_id = None 
            if not contact_id:
                contact_id = hubspot_contacts.create_hubspot_contact(email=email)
            hubspot_notes.create_hubspot_note_associated_to_contact(note_text=note_text, contact_id=contact_id)
        except HTTPError as e:
            status_code = e.response.status_code
            match status_code:
                case HTTPStatus.BAD_REQUEST:
                    logging.error(msg=f'Bad request error: {e}', stack_info=True)
                    raise HTTPException(
                        status_code=status_code, 
                        detail='Invalid data sent to API Hubspot. Please check your request data.'
                    )
                case _:
                    raise HTTPException(
                        status_code=status_code,
                        detail='An unexpected error in API Hubspot has occurred. Please contact API provider'
                    )
        except Exception as e:
            logging.error(msg=f'Unexpected error creating Hubspot note has ocurred: {e}', stack_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                detail='An unexpected internal error creating Hubspot note has ocurred. Please contact API provider'
            )
        