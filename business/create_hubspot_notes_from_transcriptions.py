from http import HTTPStatus
import logging

from fastapi import HTTPException
from business.ai.text_summarizer_service import TextSummarizerService
from business.hubspot.notes import HubspotNotes


class CreateHubspotNoteFromTranscriptionService:

    @staticmethod
    def create_hubspot_note_from_transcription(transcription:str, email:str):
        try:
            transcription = TextSummarizerService().summarize_text(transcription)
            HubspotNotes().create_hubspot_note_associated_with_a_contact_by_email(
                note_text=transcription,
                email=email
            )
        except Exception as e:
            logging.error(msg=f'Unexpected error creating Hubspot note from transcription has ocurred: {e}', stack_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                detail='An unexpected internal error creating Hubspot note from transcription has ocurred. Please contact API provider'
            )