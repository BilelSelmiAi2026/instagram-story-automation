from pathlib import Path

from PIL import UnidentifiedImageError
from requests import RequestException
from wand.exceptions import WandException

from config import (
    get_boolean_environment_variable,
    get_required_environment_variable,
)
from src.collectors.article_image_extractor import (
    ArticleImageExtractor,
)
from src.collectors.article_text_extractor import (
    ArticleTextExtractor,
)
from src.collectors.rss_collector import RSSCollector
from src.images.image_downloader import ImageDownloader
from src.images.story_carousel_generator import (
    StoryCarouselGenerator,
)
from src.images.story_image_processor import (
    StoryImageProcessor,
)
from src.images.story_slide_generator import (
    StorySlideGenerator,
)
from src.publishing.cloudinary_uploader import (
    CloudinaryUploader,
)
from src.publishing.instagram_publisher import (
    InstagramPublisher,
)
from src.storage.article_history import ArticleHistory
from src.summarizers.summarizer_factory import (
    SummarizerFactory,
)


RSS_FEED_URL = (
    "https://feeds.bbci.co.uk/news/"
    "technology/rss.xml"
)

SUMMARY_OUTPUT_FILE = Path(
    "data/output/summary.txt"
)

IMAGE_OUTPUT_DIRECTORY = Path(
    "data/output/images"
)

STORY_IMAGE_OUTPUT_FILE = Path(
    "data/output/images/story_image.jpg"
)

STORY_OUTPUT_DIRECTORY = Path(
    "data/output/stories"
)

ARTICLE_HISTORY_FILE = Path(
    "data/history/processed_articles.json"
)

SUMMARIZATION_ALGORITHM = "textrank"
LANGUAGE = "english"
SENTENCE_COUNT = 3
MAX_CHARACTERS_PER_SLIDE = 220


def save_summary(
    summary: str,
    file_path: Path,
) -> None:
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        summary,
        encoding="utf-8",
    )


def main() -> None:
    try:
        # 1. Collect the latest RSS article
        rss_collector = RSSCollector()

        article = rss_collector.collect_latest(
            feed_url=RSS_FEED_URL,
        )

        # 2. Prevent duplicate processing
        article_history = ArticleHistory(
            file_path=ARTICLE_HISTORY_FILE,
        )

        if article_history.has_been_processed(
            article_link=article.link,
        ):
            print("\nNo new article to process.")
            print(f"Already processed: {article.title}")
            return

        # 3. Extract the full article text
        article_text_extractor = ArticleTextExtractor()

        try:
            article_text = (
                article_text_extractor.extract_from_url(
                    article_url=article.link,
                )
            )

            text_source = "Full article page"

        except ValueError as extraction_error:
            print(
                "\nFull article extraction failed. "
                "Using RSS description instead."
            )
            print(f"Reason: {extraction_error}")

            article_text = article.text
            text_source = "RSS description fallback"

        # 4. Summarize the article
        summarizer = SummarizerFactory.create(
            algorithm=SUMMARIZATION_ALGORITHM,
            language=LANGUAGE,
        )

        summary = summarizer.summarize(
            text=article_text,
            sentence_count=SENTENCE_COUNT,
        )

        save_summary(
            summary=summary,
            file_path=SUMMARY_OUTPUT_FILE,
        )

        # 5. Extract the high-resolution image URL
        article_image_extractor = ArticleImageExtractor()

        high_resolution_image_url = (
            article_image_extractor.extract_from_url(
                article_url=article.link,
                fallback_image_url=article.image_url,
            )
        )

        # 6. Download the image
        image_downloader = ImageDownloader()

        downloaded_image_path = image_downloader.download(
            image_url=high_resolution_image_url,
            output_directory=IMAGE_OUTPUT_DIRECTORY,
            filename="article_image",
        )

        # 7. Crop the image to Instagram Story size
        story_image_processor = StoryImageProcessor()

        story_image_path = story_image_processor.process(
            input_path=downloaded_image_path,
            output_path=STORY_IMAGE_OUTPUT_FILE,
        )

        # 8. Generate Story carousel slides
        story_slide_generator = StorySlideGenerator()

        story_carousel_generator = StoryCarouselGenerator(
            slide_generator=story_slide_generator,
            max_characters_per_slide=(
                MAX_CHARACTERS_PER_SLIDE
            ),
        )

        story_slide_paths = (
            story_carousel_generator.generate(
                input_path=story_image_path,
                output_directory=STORY_OUTPUT_DIRECTORY,
                title=article.title,
                summary=summary,
                source=article.source,
            )
        )

        # 9. Upload Story slides to Cloudinary
        cloudinary_uploader = CloudinaryUploader(
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

        public_story_urls: list[str] = []

        for story_slide_path in story_slide_paths:
            public_url = cloudinary_uploader.upload(
                image_path=story_slide_path,
            )

            public_story_urls.append(public_url)

            print(
                f"\nUploaded {story_slide_path.name}:"
            )
            print(public_url)

        # 10. Send each public URL to Instagram
        instagram_publisher = InstagramPublisher(
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

        for public_story_url in public_story_urls:
            instagram_publisher.publish_story(
                image_url=public_story_url,
            )

        # Only mark the article after the pipeline succeeds
        article_history.mark_as_processed(
            article_link=article.link,
        )

        print("\nArticle title:\n")
        print(article.title)

        print("\nArticle source:\n")
        print(article.source)

        print("\nArticle link:\n")
        print(article.link)

        print("\nText source:\n")
        print(text_source)

        print("\nSelected image URL:\n")
        print(high_resolution_image_url)

        print(
            "\nSummarization algorithm: "
            f"{SUMMARIZATION_ALGORITHM}"
        )

        print("\nGenerated summary:\n")
        print(summary)

        print("\nGenerated Story slides:")

        for story_slide_path in story_slide_paths:
            print(story_slide_path)

        print("\nPublic Story URLs:")

        for public_story_url in public_story_urls:
            print(public_story_url)

        print("\nPipeline completed successfully.")

    except (
        FileNotFoundError,
        RequestException,
        UnidentifiedImageError,
        WandException,
        ValueError,
        OSError,
    ) as error:
        print(f"\nPipeline failed: {error}")


if __name__ == "__main__":
    main()