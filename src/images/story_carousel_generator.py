from pathlib import Path
from textwrap import wrap

from src.images.story_slide_generator import StorySlideGenerator


class StoryCarouselGenerator:
    def __init__(
        self,
        slide_generator: StorySlideGenerator,
        max_characters_per_slide: int = 260,
    ) -> None:
        if max_characters_per_slide <= 0:
            raise ValueError(
                "Maximum characters per slide "
                "must be greater than zero."
            )

        self._slide_generator = slide_generator
        self._max_characters_per_slide = (
            max_characters_per_slide
        )

    def generate(
        self,
        input_path: Path,
        output_directory: Path,
        title: str,
        summary: str,
        source: str,
    ) -> list[Path]:
        if not summary.strip():
            raise ValueError(
                "The summary cannot be empty."
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        slide_texts = self._split_summary(summary)
        total_slides = len(slide_texts)

        generated_paths: list[Path] = []

        for index, slide_text in enumerate(
            slide_texts,
            start=1,
        ):
            output_path = output_directory / (
                f"story_{index}.jpg"
            )

            progress = f"{index}/{total_slides}"

            generated_path = (
                self._slide_generator.generate(
                    input_path=input_path,
                    output_path=output_path,
                    title=title,
                    summary=slide_text,
                    source=source,
                    progress=progress,
                )
            )

            generated_paths.append(
                generated_path
            )

        return generated_paths

    def _split_summary(
        self,
        summary: str,
    ) -> list[str]:
        cleaned_summary = " ".join(
            summary.split()
        )

        chunks = wrap(
            cleaned_summary,
            width=self._max_characters_per_slide,
            break_long_words=False,
            break_on_hyphens=False,
        )

        return chunks