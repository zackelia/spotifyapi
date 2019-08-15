"""Provide the track model."""
from typing import Dict, List, Optional

from .simplified_artist import SimplifiedArtist


class Track:
    """A track."""

    def __init__(self, data):
        self._artists = [SimplifiedArtist(d) for d in data["artists"]]
        self._available_markets = (
            data["available_markets"] if "available_markets" in data else None
        )
        self._disc_number = data["disc_number"]
        self._duration_ms = data["duration_ms"]
        self._explicit = data["explicit"]
        self._external_urls = data["external_urls"]
        self._href = data["href"]
        self._id = data["id"]
        self._is_local = data["is_local"]
        self._name = data["name"]
        self._preview_url = data["preview_url"]
        self._track_number = data["track_number"]
        self._type = data["type"]
        self._uri = data["uri"]

    @property
    def artists(self) -> List[SimplifiedArtist]:
        """
        The artists who performed the track. Each artist object includes a link in href to more detailed information
        about the artist.
        """
        return self._artists

    @property
    def available_markets(self) -> Optional[List[str]]:
        """A list of the countries in which the track can be played, identified by their ISO 3166-1 alpha-2 code."""
        return self._available_markets

    @property
    def disc_number(self) -> int:
        """The disc number (usually 1 unless the album consists of more than one disc)."""
        return self._disc_number

    @property
    def duration_ms(self) -> int:
        """The track length in milliseconds."""
        return self._duration_ms

    @property
    def explicit(self) -> bool:
        """Whether or not the track has explicit lyrics ( true = yes it does; false = no it does not OR unknown)."""
        return self._explicit

    @property
    def external_urls(self) -> Dict[str, str]:
        """External URLs for this track."""
        return self._external_urls

    @property
    def href(self) -> str:
        """A link to the Web API endpoint providing full details of the track."""
        return self._href

    @property
    def id(self) -> str:
        """The Spotify ID for the track."""
        return self._id

    @property
    def is_local(self) -> bool:
        """Whether or not the track is from a local file."""
        return self._is_local

    @property
    def name(self) -> str:
        """The name of the track."""
        return self._name

    @property
    def preview_url(self) -> str:
        """A URL to a 30 second preview (MP3 format) of the track."""
        return self._preview_url

    @property
    def track_number(self) -> int:
        """
        The number of the track. If an album has several discs, the track number is the number on the specified disc.
        """
        return self._track_number

    @property
    def type(self) -> str:
        """The object type: “track”."""
        return self._type

    @property
    def uri(self) -> str:
        """The Spotify URI for the track."""
        return self._uri
