class MockParameterStore:
    def __init__(self):
        self.client = None 


    def get_parameter(self, name: str) -> str:
        """Mock function that find a parameter by name in AWS SSM Parameter Store using caching."""
        return 'test-token'
