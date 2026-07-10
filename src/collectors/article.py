from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    title: str
    text: str
    link: str
    source: str
    image_url: str