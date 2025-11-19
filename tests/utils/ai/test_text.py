import pytest
from mocks.mock_ai_text import MockTextSummarizer


# ✅ Case 1: successful summary generation
def test_summarize_text_success():
    mock_text_summarizer = MockTextSummarizer()
    result = mock_text_summarizer.summarize_text("Some text")
    assert result == "Text summary from mock"
