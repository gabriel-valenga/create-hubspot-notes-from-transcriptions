from tests.mocks.mock_ai_text import MockTextSummarizer
from business.ai.text_summarizer_service import TextSummarizerService


# Case 1: successful summary generation
def test_summarize_text_success():
    mock_text_summarizer = TextSummarizerService(MockTextSummarizer())
    result = mock_text_summarizer.summarize_text('Some text')
    assert result == 'text summary from mock'
