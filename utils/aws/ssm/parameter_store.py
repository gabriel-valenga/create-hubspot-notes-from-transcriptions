import boto3
from functools import lru_cache

class ParameterStore:
    def __init__(self):
        self.client = boto3.client("ssm")

    @lru_cache(maxsize=None)
    def get_parameter(self, name: str) -> str:
        """Find a parameter by name in AWS SSM Parameter Store using caching."""
        response = self.client.get_parameter(
            Name=name,
            WithDecryption=True
        )
        return response["Parameter"]["Value"]

# global instance
parameter_store = ParameterStore()
