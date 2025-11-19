from types import SimpleNamespace
from tests.mocks.mock_parameter_store import parameter_store

class MockTextSummarizer():

    def __init__(self):
        genai_api_key = parameter_store.get_parameter("GENAI_API_KEY")
        self.model = "mock-model"
        self.chat = "mock-chat"


    def summarize_text(self, text: str) -> str:
        """Mock function to summarize text using a mock AI service."""
        response = SimpleNamespace(text="Text summary from mock")
        print(response.text)
        try:
            return response.text
        except Exception:
            return "Error generating summary."
