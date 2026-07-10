from src.summarizers.kl_summarizer import ArticleKLSummarizer
from src.summarizers.sum_basic_summarizer import (
    ArticleSumBasicSummarizer,
)
from src.summarizers.summarizer import Summarizer
from src.summarizers.text_rank_summarizer import (
    ArticleTextRankSummarizer,
)


class SummarizerFactory:
    @staticmethod
    def create(
        algorithm: str,
        language: str = "english",
    ) -> Summarizer:
        normalized_algorithm = algorithm.strip().lower()

        if normalized_algorithm == "textrank":
            return ArticleTextRankSummarizer(
                language=language,
            )

        if normalized_algorithm in {
            "kl",
            "klsum",
            "kl-sum",
        }:
            return ArticleKLSummarizer(
                language=language,
            )

        if normalized_algorithm in {
            "sumbasic",
            "sum-basic",
            "sum_basic",
        }:
            return ArticleSumBasicSummarizer(
                language=language,
            )

        raise ValueError(
            f"Unsupported summarization algorithm: {algorithm}"
        )