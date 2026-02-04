import json
from requests import Response

def fake_response(
    status_code: int = 200,
    json_body: dict | None = None,
    text: str | None = None,
    headers: dict | None = None
):
    response = Response()
    response.status_code = status_code

    if json_body is not None:
        response._content = json.dumps(json_body).encode('utf-8')
        response.headers['Content-Type'] = 'application/json'
    elif text is not None:
        response._content = text.encode('utf-8')
    else:
        response._content = b""

    if headers is not None:
        response.headers = headers

    return response