from mock_requests import fake_response


class MockHubspotApi:

    def return_an_object_with_success():
        return fake_response(
            status_code=200,
            json_body={"id":"1", "properties":[]},
            text="ok"
        )
    

    def return_a_created_object():
        return fake_response(
            status_code=201,
            json_body={"id":"1", "properties":[]},
            text="created"
        )
    

    def return_bad_request():
        return fake_response(
            status_code=400,
            json_body={
                "status": "error",
                "message": "Fake error message",
                "correlationId": "b2c74f5e-7c2f-4fa2-a1cb-9f2fbb6e2c77",
                "category": "VALIDATION_ERROR",
                "errors": []
            },
            text="error"
        )


    def return_not_found():
        return fake_response(
            status_code=404,
            json_body={
                "status": "error",
                "message": "resource not found",
                "correlationId": "d8f9fabc-1234-5678-9999-acde48001122",
                "category": "OBJECT_NOT_FOUND"
            },
            text="not found"
        )
    

    def return_conflict_on_contact_creation():
        return fake_response(
            status_code=409,
            json_body={
                "status": "error",
                "message": "Contact already exists",
                "correlationId": "e1b9e35f-3f6e-4c89-8c3d-61a5d9b92f24",
                "category": "CONFLICT",
                "errors": [
                    {
                    "message": "A contact with this email already exists",
                    "property": "email"
                    }
                ]
            },
            text="error"
        )
    

    def return_too_many_requests():
        return fake_response(
            status_code=429,
            json_body={
                "status": "error",
                "message": "You have reached your API rate limit.",
                "correlationId": "6f3b2c9d-0e1a-4c0c-b9b5-1e6e1d9a9a12",
                "category": "RATE_LIMIT"
            },
            text="error",
            headers={
                "Retry-After": "10",
                "X-HubSpot-RateLimit-Remaining": "0",
                "X-HubSpot-RateLimit-Interval-Milliseconds": "10000",
                "X-HubSpot-Correlation-Id": "6f3b2c9d-0e1a-4c0c-b9b5-1e6e1d9a9a12",
                "Content-Type": "application/json"
            }
        )


    def return_internal_error():
        return fake_response(
            status_code=500,
            json_body={
                "status": "error",
                "message": "An unexpected error occurred",
                "correlationId": "9d7d4a20-6b99-4d9a-bf17-8c3f9fbd45c3",
                "category": "INTERNAL_ERROR"
            },
            text="internal error"
        )

