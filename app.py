from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.get("/")
def test_endpoint():
    return {"message": "Hello World"}
