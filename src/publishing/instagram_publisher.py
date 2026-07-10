from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class InstagramPublishResult:
    creation_id: str
    media_id: str


class InstagramPublisher:
    def __init__(
        self,
        instagram_account_id: str,
        access_token: str,
        api_version: str = "v24.0",
        timeout: int = 30,
        dry_run: bool = True,
    ) -> None:
        self._instagram_account_id = (
            instagram_account_id.strip()
        )
        self._access_token = access_token.strip()
        self._api_version = api_version.strip()
        self._timeout = timeout
        self._dry_run = dry_run

        self._validate_configuration()

    def publish_story(
        self,
        image_url: str,
    ) -> InstagramPublishResult | None:
        if not image_url.strip():
            raise ValueError(
                "The public image URL cannot be empty."
            )

        if not image_url.startswith(
            ("http://", "https://")
        ):
            raise ValueError(
                "Instagram requires a public HTTP or HTTPS image URL."
            )

        if self._dry_run:
            print("\nInstagram dry run")
            print(f"Would publish Story: {image_url}")
            return None

        creation_id = self._create_story_container(
            image_url=image_url,
        )

        media_id = self._publish_container(
            creation_id=creation_id,
        )

        return InstagramPublishResult(
            creation_id=creation_id,
            media_id=media_id,
        )

    def _create_story_container(
        self,
        image_url: str,
    ) -> str:
        endpoint = self._build_endpoint("media")

        response = requests.post(
            endpoint,
            data={
                "image_url": image_url,
                "media_type": "STORIES",
                "access_token": self._access_token,
            },
            timeout=self._timeout,
        )

        response.raise_for_status()

        response_data = response.json()

        creation_id = response_data.get("id", "")

        if not creation_id:
            raise ValueError(
                "Instagram did not return a creation ID."
            )

        return str(creation_id)

    def _publish_container(
        self,
        creation_id: str,
    ) -> str:
        endpoint = self._build_endpoint(
            "media_publish"
        )

        response = requests.post(
            endpoint,
            data={
                "creation_id": creation_id,
                "access_token": self._access_token,
            },
            timeout=self._timeout,
        )

        response.raise_for_status()

        response_data = response.json()

        media_id = response_data.get("id", "")

        if not media_id:
            raise ValueError(
                "Instagram did not return a media ID."
            )

        return str(media_id)

    def _build_endpoint(
        self,
        path: str,
    ) -> str:
        return (
            f"https://graph.facebook.com/"
            f"{self._api_version}/"
            f"{self._instagram_account_id}/"
            f"{path}"
        )

    def _validate_configuration(
        self,
    ) -> None:
        if not self._instagram_account_id:
            raise ValueError(
                "Instagram account ID cannot be empty."
            )

        if not self._access_token:
            raise ValueError(
                "Instagram access token cannot be empty."
            )

        if self._timeout <= 0:
            raise ValueError(
                "Timeout must be greater than zero."
            )