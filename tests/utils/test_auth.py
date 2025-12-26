import pytest
from fastapi import HTTPException
from tests.mocks.mock_auth import override_verify_token_valid, override_verify_token_invalid
from tests.mocks.mock_parameter_store import MockParameterStore
from utils.auth import hash_password, verify_password, verify_token
from utils.jwt_manager import JWTManager


mock_parameter_store = MockParameterStore()


def test_password_returns_correct_hashed_value():
    password = 'test-password'
    hashed_password = hash_password(password)
    assert hashed_password != password 
    assert isinstance(hashed_password, str)


def test_verify_password_returns_true_for_correct_password():
    password = 'test-password'
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password) is True


def test_verify_password_returns_false_for_incorrect_password():
    password = 'test-password'
    hashed_password = hash_password(password)
    assert verify_password('wrong-password', hashed_password) is False


@pytest.mark.asyncio
async def test_verify_token_success(monkeypatch):
    monkeypatch.setattr(JWTManager, 'decode_access_token', override_verify_token_valid)
    result = await verify_token('test-token')
    assert result == 'test-token'


@pytest.mark.asyncio
async def test_verify_token_error(monkeypatch):
    monkeypatch.setattr(JWTManager, 'decode_access_token', override_verify_token_invalid)
    with pytest.raises(HTTPException) as exc:
        await verify_token("bad-token")
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"

