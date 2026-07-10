from pathlib import Path

from config import (
    get_required_environment_variable,
)
from src.publishing.cloudinary_uploader import (
    CloudinaryUploader,
)


TEST_IMAGE = Path(
    "data/output/stories/story_1.jpg"
)


def main() -> None:

    uploader = CloudinaryUploader(
        cloud_name=get_required_environment_variable(
            "CLOUDINARY_CLOUD_NAME"
        ),
        api_key=get_required_environment_variable(
            "CLOUDINARY_API_KEY"
        ),
        api_secret=get_required_environment_variable(
            "CLOUDINARY_API_SECRET"
        ),
    )

    public_url = uploader.upload(
        image_path=TEST_IMAGE,
    )

    print("\nPublic URL:\n")
    print(public_url)


if __name__ == "__main__":
    main()