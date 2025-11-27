from fastapi import APIRouter, HTTPException, Request
import uuid, datetime
from models.requests.user_requests import SignupRequest, LoginRequest, TokenResponse
from utils.auth import hash_password, verify_password
from utils.storage import Storage
from utils.jwt_manager import JWTManager
from utils.rate_limiter import RateLimiter 

router = APIRouter(prefix='/auth')
jwt_manager = JWTManager()


@router.post('/signup', status_code=201)
def signup(payload: SignupRequest):
    existing = Storage.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail='User already exists')
    user_id = str(uuid.uuid4())
    hashed = hash_password(payload.password)
    Storage.create_user(user_id=user_id, email=payload.email, hashed_password=hashed)
    return {'user_id': user_id, 'email': payload.email}


@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, request: Request):
    ip = request.client.host if request.client else 'local'
    if not RateLimiter.allow_request(ip):
        raise HTTPException(status_code=429, detail='Too Many Requests')
    user = Storage.get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = jwt_manager.create_access_token(subject=user['user_id'])
    refresh_id = str(uuid.uuid4())
    expires = (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
    Storage.store_refresh_token(token_id=refresh_id, user_id=user['user_id'], expires_at_iso=expires)
    return {'access_token': access, 'token_type': 'bearer', 'refresh_token': refresh_id}


@router.post('/refresh', response_model=TokenResponse)
def refresh(refresh_token: str):
    token_item = Storage.get_refresh_token(refresh_token)
    if not token_item:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    exp = datetime.datetime.fromisoformat(token_item['expires_at'])
    if exp < datetime.datetime.now():
        Storage.delete_refresh_token(refresh_token)
        raise HTTPException(status_code=401, detail='Refresh token expired')
    access = jwt_manager.create_access_token(subject=token_item['user_id'])
    return {'access_token': access, 'token_type': 'bearer', 'refresh_token': refresh_token}


@router.post('/logout')
def logout(refresh_token: str):
    Storage.delete_refresh_token(refresh_token)
    return {'ok': True}
