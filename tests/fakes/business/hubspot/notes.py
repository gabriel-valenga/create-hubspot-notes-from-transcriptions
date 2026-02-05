class FakeHubspotNotes:

    def __init__(self):
        self.called = False 
        self.note_text = None
        self.email = None


    def create_hubspot_note_associated_with_a_contact_by_email(self, note_text:str, email:str):
        self.called = True 
        self.note_text = note_text
        self.email = email
