from sumy.summarizers.text_rank import TextRankSummarizer

from src.summarizers.base_sumy_summarizer import (
    BaseSumySummarizer,
)


class ArticleTextRankSummarizer(BaseSumySummarizer):
    def _create_summarizer(
        self,
    ) -> TextRankSummarizer:
        return TextRankSummarizer()