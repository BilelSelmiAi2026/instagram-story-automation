from pathlib import Path
from urllib.parse import urlparse

import requests


class ImageDownloader:
    def __init__(self, timeout: int = 20) -> None:
        self._timeout = timeout

    def download(
        self,
        image_url: str,
        output_directory: Path,
        filename: str = "article_image",
    ) -> Path:
        self._validate_url(image_url)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        response = requests.get(
            image_url,
            timeout=self._timeout,
            stream=True,
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            "",
        )

        if not content_type.startswith("image/"):
            raise ValueError(
                f"The URL did not return an image: {content_type}"
            )

        extension = self._get_extension(
            image_url=image_url,
            content_type=content_type,
        )

        output_path = output_directory / (
            f"{filename}{extension}"
        )

        with output_path.open("wb") as image_file:
            for chunk in response.iter_content(
                chunk_size=8192
            ):
                if chunk:
                    image_file.write(chunk)

        return output_path

    @staticmethod
    def _validate_url(image_url: str) -> None:
        if not image_url.strip():
            raise ValueError(
                "The image URL cannot be empty."
            )

        parsed_url = urlparse(image_url)

        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError(
                "The image URL must use HTTP or HTTPS."
            )

    @staticmethod
    def _get_extension(
        image_url: str,
        content_type: str,
    ) -> str:
        content_type = content_type.lower()

        extension_by_content_type = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }

        clean_content_type = content_type.split(";")[0]

        if clean_content_type in extension_by_content_type:
            return extension_by_content_type[
                clean_content_type
            ]

        url_extension = Path(
            urlparse(image_url).path
        ).suffix.lower()

        if url_extension in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }:
            return url_extension

        return ".jpg"