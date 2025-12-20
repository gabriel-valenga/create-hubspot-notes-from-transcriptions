from fastapi import HTTPException, status

async def override_verify_token_valid(token: str):
    return 'test-token'
    

async def override_verify_token_invalid(token: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token'
    )
