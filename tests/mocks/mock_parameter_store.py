class MockParameterStore:
    def __init__(self):
        self.client = None 


    def get_parameter(self, name: str) -> str:
        return 'test-token'

parameter_store = MockParameterStore()