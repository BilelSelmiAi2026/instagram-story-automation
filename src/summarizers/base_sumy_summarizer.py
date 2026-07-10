from abc import abstractmethod
from typing import Any

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from src.summarizers.summarizer import Summarizer


class BaseSumySummarizer(Summarizer):
    def __init__(self, language: str = "english") -> None:
        self._language = language
        self._summarizer = self._create_summarizer()

    @abstractmethod
    def _create_summarizer(self) -> Any:
        pass

    def summarize(
        self,
        text: str,
        sentence_count: int = 3,
    ) -> str:
        self._validate_input(
            text=text,
            sentence_count=sentence_count,
        )

        parser = PlaintextParser.from_string(
            text,
            Tokenizer(self._language),
        )

        summary_sentences = self._summarizer(
            parser.document,
            sentence_count,
        )

        return " ".join(
            str(sentence)
            for sentence in summary_sentences
        )

    @staticmethod
    def _validate_input(
        text: str,
        sentence_count: int,
    ) -> None:
        if not text.strip():
            raise ValueError(
                "The article text cannot be empty."
            )

        if sentence_count <= 0:
            raise ValueError(
                "Sentence count must be greater than zero."
            )