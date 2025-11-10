from fastapi import FastAPI, Request
from mangum import Mangum
from models.requests.text_summarizer import TextSummarizerRequest
from utils.auth import verify_token
from utils.ai.text import summarize_text

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def test_endpoint(request: Request):
    verify_token(request)
    return {"message": "Hello World"}


@app.post("/test-summarizer")
async def test_summarizer(body: TextSummarizerRequest):
    verify_token(body.request) #TO-DO: check that works
    text = body.text
    summary = summarize_text(text)
    return {"summary": summary}
