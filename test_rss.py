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

    print("\nTitle:")
    print(article.title)

    print("\nSource:")
    print(article.source)

    print("\nLink:")
    print(article.link)

    print("\nImage URL:")
    print(article.image_url)

    print("\nText:")
    print(article.text)


if __name__ == "__main__":
    main()