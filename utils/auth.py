# utils/auth.py
from fastapi import Request, HTTPException, status
from utils.aws.ssm.parameter_store import parameter_store
import os

def verify_token(request: Request):
    """Verify the Bearer token from the request against the valid token stored in AWS SSM Parameter Store."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    provided_token = auth_header.split("Bearer ")[1]
    param_name = os.getenv("AUTH_TOKEN_PARAM_NAME")

    if not param_name:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: AUTH_TOKEN_PARAM_NAME not set"
        )

    valid_token = parameter_store.get(param_name)

    if provided_token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
