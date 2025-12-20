from .mock_parameter_store import parameter_store


class JWTManager:
    
    def __init__(self):
        self.secret_key = parameter_store.get_parameter("JWT_SECRET_KEY")
        self.algorithm = "test-algorithm"


    def create_access_token(self, subject:str, expires_minutes:int=15) -> str:
        return 'test-token'
    

def override_decode_access_token_success(self, token:str)->dict:
    payload = {'sub': 'decoded-test-token', 'iat': 1, 'exp': 999999999999999}
    return payload
    

def override_decode_access_token_expired(self, token:str)->dict:
    raise Exception("Token has expired")


def override_decode_access_token_invalid(self, token:str)->dict:
    raise Exception("Invalid token")
        