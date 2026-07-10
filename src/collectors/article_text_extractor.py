from trafilatura import extract, fetch_url


class ArticleTextExtractor:
    def extract_from_url(
        self,
        article_url: str,
    ) -> str:
        if not article_url.strip():
            raise ValueError(
                "The article URL cannot be empty."
            )

        downloaded_html = fetch_url(
            article_url
        )

        if downloaded_html is None:
            raise ValueError(
                "Could not download the article page."
            )

        article_text = extract(
            downloaded_html,
            url=article_url,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        )

        if article_text is None:
            raise ValueError(
                "Could not extract readable article text."
            )

        cleaned_text = article_text.strip()

        if not cleaned_text:
            raise ValueError(
                "The extracted article text is empty."
            )

        return cleaned_text