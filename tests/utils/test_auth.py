import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from utils.auth import verify_token


# ✅ Case 1: valid token
@patch("utils.auth.parameter_store.get")
@patch("utils.auth.os.getenv")
def test_verify_token_valid(mock_getenv, mock_parameter_store_get):
    mock_getenv.return_value = "PARAM_NAME"
    mock_parameter_store_get.return_value = "valid_token"

    request = MagicMock()
    request.headers = {"Authorization": "Bearer valid_token"}

    # Should not raise any exception
    result = verify_token(request)
    assert result is None  # verify_token doesn't return anything, only raises on error


# ❌ Case 2: missing Authorization header
def test_verify_token_missing_header():
    request = MagicMock()
    request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        verify_token(request)
    assert exc_info.value.status_code == 401
    assert "Missing or invalid" in exc_info.value.detail


# ❌ Case 3: missing AUTH_TOKEN_PARAM_NAME env var
@patch("utils.auth.os.getenv", return_value=None)
def test_verify_token_missing_env(mock_getenv):
    request = MagicMock()
    request.headers = {"Authorization": "Bearer something"}

    with pytest.raises(HTTPException) as exc_info:
        verify_token(request)
    assert exc_info.value.status_code == 500
    assert "Server misconfiguration" in exc_info.value.detail


# ❌ Case 4: invalid token
@patch("utils.auth.parameter_store.get", return_value="expected_token")
@patch("utils.auth.os.getenv", return_value="PARAM_NAME")
def test_verify_token_invalid_token(mock_getenv, mock_param_get):
    request = MagicMock()
    request.headers = {"Authorization": "Bearer wrong_token"}

    with pytest.raises(HTTPException) as exc_info:
        verify_token(request)
    assert exc_info.value.status_code == 401
    assert "Invalid token" in exc_info.value.detail
