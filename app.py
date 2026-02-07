from fastapi import FastAPI, HTTPException, Request, Security, status
from fastapi.responses import JSONResponse
from mangum import Mangum
from business.create_hubspot_notes_from_transcriptions import CreateHubspotNoteFromTranscriptionService
from infra.ai.gemini_text_summarizer import GeminiTextSummarizer
from models.requests.text_summarizer import TextSummarizerRequest
from routes.auth import router as auth_router
from business.ai.text_summarizer_service import TextSummarizerService
from utils.auth import verify_token


app = FastAPI(title='Create hubspot notes from text')


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(auth_router)


@app.get("/")
def test_endpoint(request: Request, _=Security(verify_token)):
    return {"message": "Hello World"}


@app.post("/test-summarizer")
async def test_summarizer(request:Request, body: TextSummarizerRequest, _=Security(verify_token)):
    text = body.text
    summary = TextSummarizerService(GeminiTextSummarizer()).summarize_text(text)
    return {"summary": summary}


@app.post("/create-hubspot-note-from-transcription", status_code=status.HTTP_201_CREATED)
async def create_hubspot_note_from_transcription(body: dict):
    transcription = body["transcription"]
    email = body["email"]
    CreateHubspotNoteFromTranscriptionService().create_hubspot_note_from_transcription(
        transcription=transcription,
        email=email
    )
    return {"message": "Hubspot note created"}


handler = Mangum(app)
