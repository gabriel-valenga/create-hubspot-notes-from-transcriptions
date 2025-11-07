class ParameterStore:
    def __init__(self):
        self.client = None # Mock client


    def get_parameter(self, name: str) -> str:
        """Mock function that find a parameter by name in AWS SSM Parameter Store using caching."""
        # Mock response for testing purposes
        return 'test-token'

# global instance
parameter_store = ParameterStore()
