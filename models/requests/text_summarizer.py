from pydantic import BaseModel

class TextSummarizerRequest(BaseModel):
    text: str
    