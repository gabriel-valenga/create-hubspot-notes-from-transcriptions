from typing import Optional, Protocol

class StorageProtocol(Protocol):
    
    def create_user(self, user_id: str, email: str, hashed_password:str) -> None:
        """Create a new user."""
        ...


    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Retrieve a user by their email address."""
        ...
    

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Retrieve a user by their ID."""
        ...
        

    def store_refresh_token(self, token_id: str, user_id: str, expires_at_iso: str) -> None:
        """Store a refresh token."""
        ...


    def get_refresh_token(self, token_id: str) -> Optional[dict]:
        """Retrieve a refresh token by its ID."""
        ...
        

    def delete_refresh_token(self, token_id: str) -> None:
        """Delete a refresh token by its ID."""
        ...