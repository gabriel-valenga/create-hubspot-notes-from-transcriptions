import pytest
from utils.jwt_manager import JWTManager


def test_create_access_token_returns_string():
    jwtm = JWTManager()
    token = jwtm.create_access_token('test-user')
    assert isinstance(token, str)


def test_decode_access_token_success():
    jwtm = JWTManager()
    token = jwtm.create_access_token('test-user')
    payload = jwtm.decode_access_token(token)
    assert payload['sub'] == 'test-user'


def test_decode_access_token_invalid():
    jwtm = JWTManager()
    with pytest.raises(Exception) as exc:
        jwtm.decode_access_token('invalid-token')
    assert 'Invalid' in str(exc.value)


def test_decode_access_token_expired():
    jwtm = JWTManager()
    # create an already expired token
    token = jwtm.create_access_token(
        subject='test-user',
        expires_minutes=-1
    )
    with pytest.raises(Exception) as exc:
        jwtm.decode_access_token(token)
    assert str(exc.value) == 'Token has expired'
    