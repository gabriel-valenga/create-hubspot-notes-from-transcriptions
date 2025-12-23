from domain.ai.text_summarizer_protocol import TextSummarizerProtocol

class TextSummarizerService(TextSummarizerProtocol):

    def __init__(self, text_summarizer: TextSummarizerProtocol = None):
        self.text_summarizer = text_summarizer


    def summarize_text(self, text: str) -> str:
        response = self.text_summarizer.summarize_text(text)
        print(response)
        return response

