from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from utils.jwt_manager import JWTManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwtm = JWTManager()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


async def verify_token(token: str = Depends(OAuth2PasswordBearer)):
    try:
        payload = jwtm.decode_token(token)
    except ValueError as e:
        msg = str(e)
        raise HTTPException(status_code=401, detail=msg)
    return payload["sub"]
