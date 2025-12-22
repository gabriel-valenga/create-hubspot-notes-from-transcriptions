import boto3
from typing import Optional
from .storage_protocol import StorageProtocol

class DynamoStorage(StorageProtocol):

    def __init__(self):
        self.DYNAMO_TABLE_USERS = 'users'
        self.DYNAMO_TABLE_TOKENS = 'tokens'
        self.dynamodb = boto3.resource('dynamodb')
        self.users_table = self.dynamodb.Table(self.DYNAMO_TABLE_USERS)
        self.tokens_table = self.dynamodb.Table(self.DYNAMO_TABLE_TOKENS)
            

    def create_user(self,user_id: str, email: str, hashed_password:str) -> None:
        """Create a new user."""
        self.users_table.put_item(
            Item={
                'user_id': user_id,
                'email': email,
                'hashed_password': hashed_password
            }
        )

            
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Retrieve a user by their email address."""
        response = self.users_table.scan(
            FilterExpression='email = :email_value',
            ExpressionAttributeValues={':email_value': email}
        )
        items = response.get('Items', [])
        return items[0] if items else None
            
        
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Retrieve a user by their ID."""
        response = self.users_table.get_item(Key={'user_id': user_id})
        return response.get('Item')
            

    def store_refresh_token(self, token_id: str, user_id: str, expires_at_iso: str) -> None:
        """Store a refresh token."""
        item = {"token_id": token_id, "user_id": user_id, "expires_at": expires_at_iso}
        self.tokens_table.put_item(Item=item)


    def get_refresh_token(self, token_id: str) -> Optional[dict]:
        """Retrieve a refresh token by its ID."""
        resp = self.tokens_table.get_item(Key={"token_id": token_id})
        return resp.get("Item")
            

    def delete_refresh_token(self, token_id: str) -> None:
        """Delete a refresh token by its ID."""
        self.tokens_table.delete_item(Key={"token_id": token_id})
