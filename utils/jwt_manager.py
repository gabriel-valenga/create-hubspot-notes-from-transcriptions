import jwt
from datetime import datetime, timedelta
from .aws.ssm.parameter_store import parameter_store


class JWTManager:
    
    def __init__(self):
        self.secret_key = parameter_store.get_parameter("JWT_SECRET_KEY")
        self.algorithm = "HS256"


    def create_access_token(self, subject:str, expires_minutes:int=15) -> str:
        """Create a JWT access token."""
        now = datetime.now()
        expires = now + timedelta(minutes=expires_minutes)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": expires
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    

    def decode_access_token(self, token:str)->dict:
        """Decode a JWT access token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        