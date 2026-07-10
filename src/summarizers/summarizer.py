from abc import ABC, abstractmethod


class Summarizer(ABC):

    @abstractmethod
    def summarize(
        self,
        text: str,
        sentence_count: int = 3,
    ) -> str:
        pass