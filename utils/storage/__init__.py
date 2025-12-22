from config import ENV
from .local_storage import LocalStorage
from .dynamo_storage import DynamoStorage

def get_storage():
    if ENV == "local":
        return LocalStorage()
    return DynamoStorage()
