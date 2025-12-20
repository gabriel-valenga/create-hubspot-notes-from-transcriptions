import shelve
from typing import Optional
from config import ENV

class LocalStorage:
    
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