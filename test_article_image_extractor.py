from src.collectors.article_image_extractor import (
    ArticleImageExtractor,
)
from src.collectors.rss_collector import RSSCollector


RSS_FEED_URL = (
    "https://feeds.bbci.co.uk/news/"
    "technology/rss.xml"
)


def main() -> None:
    collector = RSSCollector()

    article = collector.collect_latest(
        feed_url=RSS_FEED_URL,
    )

    extractor = ArticleImageExtractor()

    high_resolution_image_url = (
        extractor.extract_from_url(
            article_url=article.link,
            fallback_image_url=article.image_url,
        )
    )

    print("\nArticle title:\n")
    print(article.title)

    print("\nRSS image URL:\n")
    print(article.image_url)

    print("\nExtracted image URL:\n")
    print(high_resolution_image_url)


if __name__ == "__main__":
    main()