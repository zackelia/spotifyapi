"""Provide the image model."""
from typing import Optional


class Image:
    """Image artwork."""

    def __init__(self, data):
        self._height = data["height"]
        self._url = data["url"]
        self._width = data["width"]

    @property
    def height(self) -> Optional[int]:
        """The image height in pixels."""
        return self._height

    @property
    def url(self) -> str:
        """The source URL of the image."""
        return self._url

    @property
    def width(self) -> Optional[int]:
        """The image width in pixels."""
        return self._width
