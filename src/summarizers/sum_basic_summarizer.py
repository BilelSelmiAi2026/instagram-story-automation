from sumy.summarizers.sum_basic import SumBasicSummarizer

from src.summarizers.base_sumy_summarizer import (
    BaseSumySummarizer,
)


class ArticleSumBasicSummarizer(BaseSumySummarizer):
    def _create_summarizer(
        self,
    ) -> SumBasicSummarizer:
        return SumBasicSummarizer()