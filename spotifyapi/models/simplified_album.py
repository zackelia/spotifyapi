"""Provide the simplified album model."""
from typing import Dict, List, Optional

from .image import Image
from .simplified_artist import SimplifiedArtist


class SimplifiedAlbum:
    """A simplified album."""

    def __init__(self, data):
        self._album_type = data["album_type"]
        self._artists = [SimplifiedArtist(d) for d in data["artists"]]
        self._available_markets = data["available_markets"] if "available_markets" in data else None
        self._external_urls = data["external_urls"]
        self._href = data["href"]
        self._id = data["id"]
        self._images = [Image(d) for d in data["images"]]
        self._name = data["name"]
        self._release_date = data["release_date"]
        self._release_date_precision = data["release_date_precision"]
        self._type = data["type"]
        self._uri = data["uri"]

    @property
    def album_type(self) -> str:
        """The type of the album: one of "album" , "single" , or "compilation"."""
        return self._album_type

    @property
    def artists(self) -> List[SimplifiedArtist]:
        """
        The artists of the album. Each artist object includes a link in href to more detailed information about the
        artist.
        """
        return self._artists

    @property
    def available_markets(self) -> Optional[List[str]]:
        """
        The markets in which the album is available: ISO 3166-1 alpha-2 country codes. Note that an album is considered
        available in a market when at least 1 of its tracks is available in that market.
        """
        return self._available_markets

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this album."""
        return self._external_urls

    @property
    def href(self) -> str:
        """A link to the Web API endpoint providing full details of the album."""
        return self._href

    @property
    def id(self) -> str:
        """The Spotify ID for the album."""
        return self._id

    @property
    def images(self) -> List[Image]:
        """The cover art for the album in various sizes, widest first."""
        return self._images

    @property
    def name(self) -> str:
        """The name of the album. In case of an album takedown, the value may be an empty string."""
        return self._name

    @property
    def release_date(self) -> str:
        """
        The date the album was first released, for example 1981. Depending on the precision, it might be shown as
        1981-12 or 1981-12-15.
        """
        return self._release_date

    @property
    def release_date_precision(self) -> str:
        """The precision with which release_date value is known: year, month, or day."""
        return self._release_date_precision

    @property
    def type(self) -> str:
        """The object type: “album”"""
        return self._type

    @property
    def uri(self) -> str:
        """The Spotify URI for the album."""
        return self._uri
