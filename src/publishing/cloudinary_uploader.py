from pathlib import Path

import cloudinary
import cloudinary.uploader

from src.publishing.image_uploader import (
    ImageUploader,
)


class CloudinaryUploader(ImageUploader):
    def __init__(
        self,
        cloud_name: str,
        api_key: str,
        api_secret: str,
    ) -> None:

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    def upload(
        self,
        image_path: Path,
    ) -> str:

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        upload_result = cloudinary.uploader.upload(
            str(image_path),
            folder="instagram-story-bot",
            overwrite=True,
        )

        secure_url = upload_result.get(
            "secure_url",
            "",
        )

        if not secure_url:
            raise ValueError(
                "Cloudinary did not return a public URL."
            )

        return str(secure_url)