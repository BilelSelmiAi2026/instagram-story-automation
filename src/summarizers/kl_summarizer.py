from sumy.summarizers.kl import KLSummarizer

from src.summarizers.base_sumy_summarizer import (
    BaseSumySummarizer,
)


class ArticleKLSummarizer(BaseSumySummarizer):
    def _create_summarizer(
        self,
    ) -> KLSummarizer:
        return KLSummarizer()