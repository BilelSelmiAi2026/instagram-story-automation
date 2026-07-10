from abc import ABC, abstractmethod
from pathlib import Path


class ImageUploader(ABC):
    @abstractmethod
    def upload(
        self,
        image_path: Path,
    ) -> str:
        """
        Upload an image and return its public HTTPS URL.
        """
        pass