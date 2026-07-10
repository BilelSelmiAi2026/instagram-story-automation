from src.collectors.article_text_extractor import (
    ArticleTextExtractor,
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

    extractor = ArticleTextExtractor()

    full_text = extractor.extract_from_url(
        article_url=article.link,
    )

    print("\nTitle:\n")
    print(article.title)

    print("\nRSS description:\n")
    print(article.text)

    print("\nExtracted full article:\n")
    print(full_text)

    print("\nCharacter count:")
    print(len(full_text))


if __name__ == "__main__":
    main()