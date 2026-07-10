from config import (
    get_boolean_environment_variable,
    get_required_environment_variable,
)
from src.publishing.instagram_publisher import (
    InstagramPublisher,
)


TEST_PUBLIC_IMAGE_URL = (
    "https://example.com/story_1.jpg"
)


def main() -> None:
    publisher = InstagramPublisher(
        instagram_account_id=(
            get_required_environment_variable(
                "INSTAGRAM_ACCOUNT_ID"
            )
        ),
        access_token=(
            get_required_environment_variable(
                "INSTAGRAM_ACCESS_TOKEN"
            )
        ),
        api_version=(
            get_required_environment_variable(
                "INSTAGRAM_API_VERSION"
            )
        ),
        dry_run=get_boolean_environment_variable(
            "INSTAGRAM_DRY_RUN",
            default=True,
        ),
    )

    publisher.publish_story(
        image_url=TEST_PUBLIC_IMAGE_URL,
    )


if __name__ == "__main__":
    main()