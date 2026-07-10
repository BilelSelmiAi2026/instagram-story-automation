from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class ArticleImageExtractor:
    def __init__(self, timeout: int = 20) -> None:
        self._timeout = timeout

    def extract_from_url(
        self,
        article_url: str,
        fallback_image_url: str = "",
    ) -> str:
        self._validate_url(article_url)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(
                article_url,
                headers=headers,
                timeout=self._timeout,
            )

            response.raise_for_status()

        except requests.RequestException:
            if fallback_image_url.strip():
                return fallback_image_url

            raise ValueError(
                "Could not download the article page "
                "and no fallback image was provided."
            )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        image_url = (
            self._extract_open_graph_image(soup)
            or self._extract_twitter_image(soup)
            or self._extract_first_article_image(soup)
        )

        if not image_url:
            if fallback_image_url.strip():
                return fallback_image_url

            raise ValueError(
                "Could not find an article image."
            )

        return urljoin(
            article_url,
            image_url,
        )

    @staticmethod
    def _extract_open_graph_image(
        soup: BeautifulSoup,
    ) -> str:
        tag = soup.find(
            "meta",
            attrs={"property": "og:image"},
        )

        if tag is None:
            return ""

        content = tag.get("content", "")

        return str(content).strip()

    @staticmethod
    def _extract_twitter_image(
        soup: BeautifulSoup,
    ) -> str:
        tag = soup.find(
            "meta",
            attrs={"name": "twitter:image"},
        )

        if tag is None:
            tag = soup.find(
                "meta",
                attrs={"property": "twitter:image"},
            )

        if tag is None:
            return ""

        content = tag.get("content", "")

        return str(content).strip()

    @staticmethod
    def _extract_first_article_image(
        soup: BeautifulSoup,
    ) -> str:
        article = soup.find("article")

        if article is None:
            return ""

        image = article.find("img")

        if image is None:
            return ""

        src = image.get("src", "")

        if src:
            return str(src).strip()

        srcset = image.get("srcset", "")

        if not srcset:
            return ""

        candidates = str(srcset).split(",")

        if not candidates:
            return ""

        last_candidate = candidates[-1].strip()

        return last_candidate.split(" ")[0]

    @staticmethod
    def _validate_url(
        article_url: str,
    ) -> None:
        if not article_url.strip():
            raise ValueError(
                "The article URL cannot be empty."
            )

        if not article_url.startswith(
            ("http://", "https://")
        ):
            raise ValueError(
                "The article URL must use HTTP or HTTPS."
            )