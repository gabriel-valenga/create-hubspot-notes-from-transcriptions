import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from models.requests.user_requests import SignupRequest, LoginRequest, TokenResponse
from utils.auth import hash_password, verify_password
from utils.storage import get_storage
from utils.jwt_manager import JWTManager
from utils.rate_limiter.local_rate_limiter import LocalRateLimiter 

router = APIRouter(prefix='/auth')
jwt_manager = JWTManager()
storage = get_storage()

@router.post('/signup', status_code=201)
def signup(payload: SignupRequest):
    existing = storage.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail='User already exists')
    user_id = str(uuid.uuid4())
    hashed = hash_password(payload.password)
    storage.create_user(user_id=user_id, email=payload.email, hashed_password=hashed)
    return {'user_id': user_id, 'email': payload.email}


@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, _: Request):
    email = payload.email.lower()
    if not LocalRateLimiter().allow_request(email):
        raise HTTPException(status_code=429, detail='Too Many Requests')
    user = storage.get_user_by_email(payload.email)        
    if not user or not verify_password(payload.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = jwt_manager.create_access_token(subject=user['user_id'])
    refresh_id = str(uuid.uuid4())
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    storage.store_refresh_token(token_id=refresh_id, user_id=user['user_id'], expires_at_iso=expires)
    return {'access_token': access, 'token_type': 'bearer', 'refresh_token': refresh_id}


@router.post('/refresh', response_model=TokenResponse)
def refresh(refresh_token: str):
    token_item = storage.get_refresh_token(refresh_token)
    if not token_item:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    exp = datetime.fromisoformat(token_item['expires_at'])
    if exp < datetime.now(timezone.utc):
        storage.delete_refresh_token(refresh_token)
        raise HTTPException(status_code=401, detail='Refresh token expired')
    access = jwt_manager.create_access_token(subject=token_item['user_id'])
    return {'access_token': access, 'token_type': 'bearer', 'refresh_token': refresh_token}


@router.post('/logout')
def logout(refresh_token: str):
    storage.delete_refresh_token(refresh_token)
    return {'ok': True}


@router.post('/login-swagger', response_model=TokenResponse)
def login_swagger(form: OAuth2PasswordRequestForm = Depends()):
    email = form.username.lower()
    if not LocalRateLimiter().allow_request(email):
        raise HTTPException(status_code=429, detail='Too Many Requests')
    user = storage.get_user_by_email(email)
    if not user or not verify_password(form.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = jwt_manager.create_access_token(subject=user['user_id'])
    refresh_id = str(uuid.uuid4())
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    storage.store_refresh_token(token_id=refresh_id, user_id=user['user_id'], expires_at_iso=expires)
    return {'access_token': access, 'token_type': 'bearer', 'refresh_token': refresh_id}
