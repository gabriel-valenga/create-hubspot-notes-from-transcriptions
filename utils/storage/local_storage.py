import shelve
from typing import Optional
from .storage_protocol import StorageProtocol

class LocalStorage(StorageProtocol):
    
    def __init__(self):
        self._USERS_DB = 'local_users.db'
        self._TOKENS_DB = 'local_tokens.db'


    def create_user(self, user_id: str, email: str, hashed_password:str) -> None:
        """Create a new user."""
        with shelve.open(self._USERS_DB) as db:
            if user_id in db:
                raise ValueError('User already exists')
            db[user_id] = {'user_id': user_id, 'email': email, 'hashed_password': hashed_password}


    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Retrieve a user by their email address."""
        with shelve.open(self._USERS_DB) as db:
            for user in db.values():
                if user['email'] == email:
                    return user
        return None
    

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Retrieve a user by their ID."""
        with shelve.open(self._USERS_DB) as db:
            return db.get(user_id)
        

    def store_refresh_token(self, token_id: str, user_id: str, expires_at_iso: str) -> None:
        """Store a refresh token."""
        item = {"token_id": token_id, "user_id": user_id, "expires_at": expires_at_iso}
        with shelve.open(self._TOKENS_DB) as db:
            db[token_id] = item


    def get_refresh_token(self, token_id: str) -> Optional[dict]:
        """Retrieve a refresh token by its ID."""
        with shelve.open(self._TOKENS_DB) as db:
            return db.get(token_id)
        

    def delete_refresh_token(self, token_id: str) -> None:
        """Delete a refresh token by its ID."""
        with shelve.open(self._TOKENS_DB) as db:
            if token_id in db:
                del db[token_id]