from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from mangum import Mangum
from models.requests.text_summarizer import TextSummarizerRequest
from routes.auth import router as auth_router
from utils.ai.text import TextSummarizer
from utils.auth import verify_token


app = FastAPI(title='Create hubspot notes from text')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login") # OAuth2 scheme setup, points to the token URL for Swagger UI "Authorize" button


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


@app.get("/", dependencies=[Depends(verify_token)])
def test_endpoint(request: Request):
    return {"message": "Hello World"}


@app.post("/test-summarizer", dependencies=[Depends(verify_token)])
async def test_summarizer(request:Request, body: TextSummarizerRequest):
    text = body.text
    summary = TextSummarizer().summarize_text(text)
    return {"summary": summary}


handler = Mangum(app)
