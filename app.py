from fastapi import FastAPI
from mangum import Mangum
from .utils.ai.text import summarize_text

app = FastAPI()
handler = Mangum(app)

app.get("/")
def test_endpoint():
    return {"message": "Hello World"}


# app.py

@app.route('/test-text-summarizer', methods=['POST'])
def test_text_summarizer():
    request = app.current_request
    body = request.json_body
    text = body.get("text", "")
    summary = summarize_text(text)
    return {"summary": summary}
