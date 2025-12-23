from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.responses import JSONResponse
from mangum import Mangum
from models.requests.text_summarizer import TextSummarizerRequest
from routes.auth import router as auth_router
from business.ai.text_summarizer_service import TextSummarizer
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
    summary = TextSummarizer().summarize_text(text)
    return {"summary": summary}


handler = Mangum(app)
