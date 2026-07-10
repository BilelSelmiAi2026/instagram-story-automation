import json
from pathlib import Path
from typing import Any


class ArticleHistory:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def has_been_processed(
        self,
        article_link: str,
    ) -> bool:
        self._validate_link(article_link)

        processed_links = self._load_links()

        return article_link in processed_links

    def mark_as_processed(
        self,
        article_link: str,
    ) -> None:
        self._validate_link(article_link)

        processed_links = self._load_links()

        if article_link in processed_links:
            return

        processed_links.append(article_link)

        self._save_links(processed_links)

    def _load_links(self) -> list[str]:
        if not self._file_path.exists():
            return []

        try:
            content = self._file_path.read_text(
                encoding="utf-8",
            )

            if not content.strip():
                return []

            data: Any = json.loads(content)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The article history file contains invalid JSON."
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                "The article history file must contain a list."
            )

        return [
            str(link)
            for link in data
            if isinstance(link, str)
        ]

    def _save_links(
        self,
        processed_links: list[str],
    ) -> None:
        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file_path.write_text(
            json.dumps(
                processed_links,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _validate_link(
        article_link: str,
    ) -> None:
        if not article_link.strip():
            raise ValueError(
                "The article link cannot be empty."
            )