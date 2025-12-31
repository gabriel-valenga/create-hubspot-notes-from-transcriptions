def override_verify_token_valid(self, token: str):
    return {"sub": "test-token"}
    

def override_verify_token_invalid(self, token: str):
    raise ValueError("Invalid token")
