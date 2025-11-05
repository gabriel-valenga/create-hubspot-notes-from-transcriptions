from fastapi import FastAPI, Request
from mangum import Mangum
from utils.auth import verify_token
from .utils.ai.text import summarize_text

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def test_endpoint(request: Request):
    verify_token(request)
    return {"message": "Hello World"}


@app.post("/test-summarizer")
async def test_summarizer(request: Request):
    verify_token(request)
    body = await request.json()
    text = body.get("text", "")
    summary = summarize_text(text)
    return {"summary": summary}