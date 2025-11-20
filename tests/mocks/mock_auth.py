from tests.mocks.mock_parameter_store import MockParameterStore
from fastapi import HTTPException, status
import os

mock_parameter_store = MockParameterStore()

def mock_verify_token(request, simulate_missing_env=False, simulate_invalid_token=False):
    """Mock function to verify the Bearer token from the request against the valid token stored in mock parameter store."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    if simulate_missing_env:
        param_name = None
    else:
        param_name = "test-token"

    provided_token = "test-token" if not simulate_invalid_token else "wrong-token"

    if not param_name:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: AUTH_TOKEN_PARAM_NAME not set"
        )

    valid_token = mock_parameter_store.get_parameter(param_name)

    if provided_token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
