from types import SimpleNamespace
from tests.mocks.mock_parameter_store import MockParameterStore

class MockTextSummarizer():

    def __init__(self):
        mock_parameter_store = MockParameterStore()
        genai_api_key = mock_parameter_store.get_parameter("GENAI_API_KEY")
        self.model = "mock-model"
        self.chat = "mock-chat"


    def summarize_text(self, text: str) -> str:
        """Mock function to summarize text using a mock AI service."""
        response = SimpleNamespace(text="Text summary from mock")
        print(response.text)
        return response.text
