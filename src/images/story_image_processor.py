from pathlib import Path

from PIL import Image, ImageOps


class StoryImageProcessor:
    STORY_WIDTH = 1080
    STORY_HEIGHT = 1920

    def process(
        self,
        input_path: Path,
        output_path: Path,
    ) -> Path:
        if not input_path.exists():
            raise FileNotFoundError(
                f"Input image was not found: {input_path}"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with Image.open(input_path) as image:
            image = image.convert("RGB")

            processed_image = ImageOps.fit(
                image,
                (
                    self.STORY_WIDTH,
                    self.STORY_HEIGHT,
                ),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )

            processed_image.save(
                output_path,
                format="JPEG",
                quality=95,
            )

        return output_path