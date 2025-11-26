import boto3
import os 
from functools import lru_cache
from config import ENV


class ParameterStore:

    def __init__(self):
        if ENV != 'local':
            self.client = boto3.client("ssm")


    @lru_cache(maxsize=None)
    def get_parameter(self, name: str) -> str:
        """Find a parameter by name in AWS SSM Parameter Store using caching."""
        if ENV == 'local':
            value = os.getenv(name)
            if value is None:
                raise RuntimeError(f"Parameter {name} not found in environment variables.")
            return value
        response = self.client.get_parameter(
            Name=name,
            WithDecryption=True
        )
        return response["Parameter"]["Value"]

# global instance
parameter_store = ParameterStore()
