from fastapi import FastAPI, Request
from mangum import Mangum
from models.requests.text_summarizer import TextSummarizerRequest
from utils.auth import verify_token
from utils.ai.text import TextSummarizer

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def test_endpoint(request: Request):
    verify_token(request)
    return {"message": "Hello World"}


@app.post("/test-summarizer")
async def test_summarizer(request:Request, body: TextSummarizerRequest):
    verify_token(request)
    text = body.text
    summary = TextSummarizer().summarize_text(text)
    return {"summary": summary}
