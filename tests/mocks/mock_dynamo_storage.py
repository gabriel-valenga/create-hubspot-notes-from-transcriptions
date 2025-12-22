from typing import Optional
from utils.storage.storage_protocol import StorageProtocol

class FakeDynamoStorage(StorageProtocol):

    def __init__(self):
        self.users_table: dict[str, dict] = {}
        self.tokens_table: dict[str, dict] = {}
            

    def create_user(self,user_id: str, email: str, hashed_password:str) -> None:
        if user_id in self.users_table:
            raise ValueError("User already exists")
        self.users_table[user_id] = {
            'user_id': user_id,
            'email': email,
            'hashed_password': hashed_password
        }

            
    def get_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users_table.values():
            if user['email'] == email:
                return user
        return None   
        
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users_table.get(user_id, None)


    def store_refresh_token(self, token_id: str, user_id: str, expires_at_iso: str) -> None:
        item = {"token_id": token_id, "user_id": user_id, "expires_at": expires_at_iso}
        self.tokens_table[token_id] = item


    def get_refresh_token(self, token_id: str) -> Optional[dict]:
        return self.tokens_table.get(token_id, None)
    

    def delete_refresh_token(self, token_id: str) -> None:
        self.tokens_table.pop(token_id, None)
