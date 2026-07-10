import platform
from pathlib import Path
from textwrap import wrap

from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


class StorySlideGenerator:
    STORY_WIDTH = 1080
    STORY_HEIGHT = 1920

    def __init__(
        self,
        regular_font_path: str | None = None,
        bold_font_path: str | None = None,
    ) -> None:
        default_regular_font, default_bold_font = (
            self._get_default_font_paths()
        )

        self._regular_font_path = (
            regular_font_path or default_regular_font
        )

        self._bold_font_path = (
            bold_font_path or default_bold_font
        )

    def generate(
        self,
        input_path: Path,
        output_path: Path,
        title: str,
        summary: str,
        source: str,
        progress: str = "",
    ) -> Path:
        self._validate_input(
            input_path=input_path,
            title=title,
            summary=summary,
            source=source,
        )

        self._validate_fonts()

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with Image(filename=str(input_path)) as image:
            image.resize(
                self.STORY_WIDTH,
                self.STORY_HEIGHT,
            )

            self._add_dark_overlay(image)
            self._draw_category(image)

            self._draw_title(
                image=image,
                title=title,
            )

            self._draw_summary(
                image=image,
                summary=summary,
            )

            self._draw_source(
                image=image,
                source=source,
            )

            if progress.strip():
                self._draw_progress(
                    image=image,
                    progress=progress,
                )

            image.format = "jpeg"
            image.compression_quality = 95
            image.save(filename=str(output_path))

        return output_path

    def _add_dark_overlay(
        self,
        image: Image,
    ) -> None:
        with Drawing() as drawing:
            drawing.fill_color = Color(
                "rgba(0, 0, 0, 0.80)"
            )

            drawing.rectangle(
                left=0,
                top=850,
                right=self.STORY_WIDTH,
                bottom=self.STORY_HEIGHT,
            )

            drawing(image)

    def _draw_category(
        self,
        image: Image,
    ) -> None:
        with Drawing() as drawing:
            drawing.font = self._bold_font_path
            drawing.font_size = 28
            drawing.fill_color = Color(
                "rgba(255, 255, 255, 0.75)"
            )
            drawing.text_antialias = True

            drawing.text(
                70,
                950,
                "AI NEWS",
            )

            drawing(image)

    def _draw_title(
        self,
        image: Image,
        title: str,
    ) -> None:
        lines = self._wrap_text(
            text=title,
            max_characters=25,
        )

        with Drawing() as drawing:
            drawing.font = self._bold_font_path
            drawing.font_size = 66
            drawing.fill_color = Color("white")
            drawing.text_antialias = True

            start_y = 1040
            line_height = 78

            for index, line in enumerate(lines[:3]):
                drawing.text(
                    70,
                    start_y + index * line_height,
                    line,
                )

            drawing(image)

    def _draw_summary(
        self,
        image: Image,
        summary: str,
    ) -> None:
        lines = self._wrap_text(
            text=summary,
            max_characters=38,
        )

        with Drawing() as drawing:
            drawing.font = self._regular_font_path
            drawing.font_size = 42
            drawing.fill_color = Color(
                "rgba(255, 255, 255, 0.92)"
            )
            drawing.text_antialias = True

            start_y = 1320
            line_height = 56

            for index, line in enumerate(lines[:7]):
                drawing.text(
                    70,
                    start_y + index * line_height,
                    line,
                )

            drawing(image)

    def _draw_source(
        self,
        image: Image,
        source: str,
    ) -> None:
        with Drawing() as drawing:
            drawing.font = self._regular_font_path
            drawing.font_size = 28
            drawing.fill_color = Color(
                "rgba(255, 255, 255, 0.65)"
            )
            drawing.text_antialias = True

            drawing.text(
                70,
                1810,
                f"Source: {source}",
            )

            drawing(image)

    def _draw_progress(
        self,
        image: Image,
        progress: str,
    ) -> None:
        with Drawing() as drawing:
            drawing.font = self._bold_font_path
            drawing.font_size = 28
            drawing.fill_color = Color(
                "rgba(255, 255, 255, 0.75)"
            )
            drawing.text_antialias = True

            drawing.text(
                930,
                1810,
                progress,
            )

            drawing(image)

    def _validate_fonts(self) -> None:
        font_paths = [
            Path(self._regular_font_path),
            Path(self._bold_font_path),
        ]

        for font_path in font_paths:
            if not font_path.exists():
                raise FileNotFoundError(
                    f"Font file was not found: {font_path}"
                )

    @staticmethod
    def _get_default_font_paths() -> tuple[str, str]:
        operating_system = platform.system()

        if operating_system == "Darwin":
            return (
                (
                    "/System/Library/Fonts/"
                    "Supplemental/Arial.ttf"
                ),
                (
                    "/System/Library/Fonts/"
                    "Supplemental/Arial Bold.ttf"
                ),
            )

        if operating_system == "Linux":
            return (
                (
                    "/usr/share/fonts/truetype/"
                    "liberation/"
                    "LiberationSans-Regular.ttf"
                ),
                (
                    "/usr/share/fonts/truetype/"
                    "liberation/"
                    "LiberationSans-Bold.ttf"
                ),
            )

        raise OSError(
            f"Unsupported operating system: {operating_system}"
        )

    @staticmethod
    def _wrap_text(
        text: str,
        max_characters: int,
    ) -> list[str]:
        return wrap(
            text.strip(),
            width=max_characters,
            break_long_words=False,
            break_on_hyphens=False,
        )

    @staticmethod
    def _validate_input(
        input_path: Path,
        title: str,
        summary: str,
        source: str,
    ) -> None:
        if not input_path.exists():
            raise FileNotFoundError(
                f"Story image was not found: {input_path}"
            )

        if not title.strip():
            raise ValueError(
                "The title cannot be empty."
            )

        if not summary.strip():
            raise ValueError(
                "The summary cannot be empty."
            )

        if not source.strip():
            raise ValueError(
                "The source cannot be empty."
            )