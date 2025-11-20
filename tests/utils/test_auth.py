import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from tests.mocks.mock_auth import mock_verify_token
from tests.mocks.mock_parameter_store import MockParameterStore


mock_parameter_store = MockParameterStore()

# ✅ Case 1: valid token (using our mock)
def test_mock_verify_token_valid():
    request = MagicMock()
    request.headers = {"Authorization": "Bearer valid_token"}

    result = mock_verify_token(request)
    assert result is None  # Should not raise exception


# ❌ Case 2: missing Authorization header
def test_mock_verify_token_missing_header():
    request = MagicMock()
    request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        mock_verify_token(request)
    assert "Missing or invalid" in exc_info.value.detail


# ❌ Case 3: missing AUTH_TOKEN_PARAM_NAME env var
def test_mock_verify_token_missing_env():
    request = MagicMock()
    request.headers = {"Authorization": "Bearer something"}

    with pytest.raises(HTTPException) as exc_info:
        mock_verify_token(request, simulate_missing_env=True)
    assert exc_info.value.status_code == 500
    assert "Server misconfiguration" in exc_info.value.detail


# ❌ Case 4: invalid token
def test_mock_verify_token_invalid_token():
    request = MagicMock()
    request.headers = {"Authorization": "Bearer wrong_token"}

    with pytest.raises(HTTPException) as exc_info:
        mock_verify_token(request, simulate_invalid_token=True)
    assert "Invalid token" in exc_info.value.detail
