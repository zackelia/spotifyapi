"""Provide the artist model."""
from typing import Dict


class Artist:
    """An artist."""

    def __init__(self, data):
        self._external_urls = data["external_urls"]
        self._href = data["href"]
        self._id = data["id"]
        self._name = data["name"]
        self._type = data["type"]
        self._uri = data["uri"]

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this artist."""
        return self._external_urls

    @property
    def href(self) -> str:
        """A link to the Web API endpoint providing full details of the artist."""
        return self._href

    @property
    def id(self) -> str:
        """The Spotify ID for the artist."""
        return self._id

    @property
    def name(self) -> str:
        """The name of the artist."""
        return self._name

    @property
    def type(self) -> str:
        """The object type: "artist"."""
        return self._type

    @property
    def uri(self) -> str:
        """The Spotify URI for the artist."""
        return self._uri
