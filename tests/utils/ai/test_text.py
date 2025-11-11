import pytest
from unittest.mock import MagicMock, patch
from utils.ai.text import TextSummarizer


# ✅ Case 1: model initialized successfully
@patch("utils.ai.text.parameter_store.get_parameter", return_value="fake_api_key")
@patch("utils.ai.text.genai.configure")
@patch("utils.ai.text.genai.GenerativeModel")
def test_textsummarizer_init(mock_model_class, mock_genai_configure, mock_get_parameter):
    # Mock GenerativeModel and chat instance
    mock_chat_instance = MagicMock()
    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat_instance
    mock_model_class.return_value = mock_model_instance

    summarizer = TextSummarizer()

    # Assertions
    mock_get_parameter.assert_called_once_with("GENAI_API_KEY")
    mock_genai_configure.assert_called_once_with(api_key="fake_api_key")
    mock_model_class.assert_called_once_with("models/gemini-2.5-flash-lite")
    mock_model_instance.start_chat.assert_called_once()
    assert summarizer.chat == mock_chat_instance


# ✅ Case 2: summarize_text returns response text successfully
@patch("utils.ai.text.parameter_store.get_parameter", return_value="fake_api_key")
@patch("utils.ai.text.genai.configure")
@patch("utils.ai.text.genai.GenerativeModel")
def test_summarize_text_success(mock_model_class, mock_genai_configure, mock_get_parameter):
    # Mock chat and response
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a summary."
    mock_chat.send_message.return_value = mock_response

    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat
    mock_model_class.return_value = mock_model_instance

    summarizer = TextSummarizer()
    summary = summarizer.summarize_text("Long text to summarize.")

    mock_chat.send_message.assert_called_once()
    assert summary == "This is a summary."


# ❌ Case 3: summarize_text handles exception gracefully
@patch("utils.ai.text.parameter_store.get_parameter", return_value="fake_api_key")
@patch("utils.ai.text.genai.configure")
@patch("utils.ai.text.genai.GenerativeModel")
def test_summarize_text_exception(mock_model_class, mock_genai_configure, mock_get_parameter):
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = None  # Simulate missing text
    mock_chat.send_message.return_value = mock_response

    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat
    mock_model_class.return_value = mock_model_instance

    summarizer = TextSummarizer()
    summary = summarizer.summarize_text("Some text")

    assert summary == "Error generating summary."
