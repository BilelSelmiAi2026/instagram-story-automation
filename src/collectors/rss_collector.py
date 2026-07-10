from typing import Any

import feedparser
from bs4 import BeautifulSoup

from src.collectors.article import Article


class RSSCollector:
    def collect_latest(
        self,
        feed_url: str,
    ) -> Article:
        if not feed_url.strip():
            raise ValueError(
                "The RSS feed URL cannot be empty."
            )

        feed = feedparser.parse(feed_url)

        if getattr(feed, "bozo", False):
            exception = getattr(
                feed,
                "bozo_exception",
                None,
            )

            if not feed.entries:
                raise ValueError(
                    f"Could not parse RSS feed: {exception}"
                )

        if not feed.entries:
            raise ValueError(
                "The RSS feed contains no articles."
            )

        entry = feed.entries[0]

        title = self._get_required_value(
            entry=entry,
            key="title",
        )

        link = self._get_required_value(
            entry=entry,
            key="link",
        )

        text = self._extract_text(entry)

        source = self._extract_source(
            feed=feed,
        )

        image_url = self._extract_image_url(
            entry=entry,
        )

        if not image_url:
            raise ValueError(
                "The latest RSS article has no image."
            )

        return Article(
            title=title,
            text=text,
            link=link,
            source=source,
            image_url=image_url,
        )

    def _extract_text(
        self,
        entry: Any,
    ) -> str:
        raw_text = ""

        content = entry.get("content")

        if content:
            raw_text = content[0].get(
                "value",
                "",
            )

        if not raw_text:
            raw_text = entry.get(
                "summary",
                "",
            )

        clean_text = BeautifulSoup(
            raw_text,
            "html.parser",
        ).get_text(
            separator=" ",
            strip=True,
        )

        if not clean_text:
            raise ValueError(
                "The RSS article contains no usable text."
            )

        return clean_text

    def _extract_source(
        self,
        feed: Any,
    ) -> str:
        feed_title = feed.feed.get(
            "title",
            "",
        ).strip()

        return feed_title or "Unknown source"

    def _extract_image_url(
        self,
        entry: Any,
    ) -> str:
        media_content = entry.get(
            "media_content",
            [],
        )

        for media_item in media_content:
            image_url = media_item.get(
                "url",
                "",
            )

            if image_url:
                return image_url

        media_thumbnail = entry.get(
            "media_thumbnail",
            [],
        )

        for thumbnail in media_thumbnail:
            image_url = thumbnail.get(
                "url",
                "",
            )

            if image_url:
                return image_url

        enclosures = entry.get(
            "enclosures",
            [],
        )

        for enclosure in enclosures:
            enclosure_type = enclosure.get(
                "type",
                "",
            )

            image_url = enclosure.get(
                "href",
                "",
            )

            if (
                enclosure_type.startswith("image/")
                and image_url
            ):
                return image_url

        return ""

    @staticmethod
    def _get_required_value(
        entry: Any,
        key: str,
    ) -> str:
        value = entry.get(
            key,
            "",
        ).strip()

        if not value:
            raise ValueError(
                f"The RSS article has no {key}."
            )

        return value