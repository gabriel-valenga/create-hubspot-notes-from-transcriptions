




class DynamoStorage:

    def __init__(self):
        self.ENV = ENV
        self.DYNAMO_TABLE_USERS = 'users'
        self.DYNAMO_TABLE_TOKENS = 'tokens'

        if selfENV != 'local':
            import boto3
            dynamodb = boto3.resource('dynamodb')
            users_table = dynamodb.Table(self.DYNAMO_TABLE_USERS)
            tokens_table = dynamodb.Table(self.DYNAMO_TABLE_TOKENS)
        # else:
            

    @staticmethod
    def create_user(user_id: str, email: str, hashed_password:str) -> None:
        """Create a new user."""
        if ENV != 'local':
            users_table.put_item(
                Item={
                    'user_id': user_id,
                    'email': email,
                    'hashed_password': hashed_password
                }
            )
        # else:
            


    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        """Retrieve a user by their email address."""
        if ENV != 'local':
            response = users_table.scan(
                FilterExpression='email = :email_value',
                ExpressionAttributeValues={':email_value': email}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        else:
            
        

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[dict]:
        """Retrieve a user by their ID."""
        if ENV != 'local':
            response = users_table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        else:
            with shelve.open(_USERS_DB) as db:
                return db.get(user_id)
            

    @staticmethod
    def store_refresh_token(token_id: str, user_id: str, expires_at_iso: str) -> None:
        """Store a refresh token."""
        item = {"token_id": token_id, "user_id": user_id, "expires_at": expires_at_iso}
        if ENV != "local":
            tokens_table.put_item(Item=item)
        else:
            with shelve.open(_TOKENS_DB) as db:
                db[token_id] = item


    @staticmethod
    def get_refresh_token(token_id: str) -> Optional[dict]:
        """Retrieve a refresh token by its ID."""
        if ENV != "local":
            resp = tokens_table.get_item(Key={"token_id": token_id})
            return resp.get("Item")
        else:
            with shelve.open(_TOKENS_DB) as db:
                return db.get(token_id)
            

    @staticmethod
    def delete_refresh_token(token_id: str):
        """Delete a refresh token by its ID."""
        if ENV != "local":
            tokens_table.delete_item(Key={"token_id": token_id})
        else:
            with shelve.open(_TOKENS_DB) as db:
                if token_id in db:
                    del db[token_id]
