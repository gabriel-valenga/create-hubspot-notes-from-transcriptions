from typing import Protocol


class TextSummarizerProtocol(Protocol):

    def summarize_text(self, text: str) -> str:
        ...
        