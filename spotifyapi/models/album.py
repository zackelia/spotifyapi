"""Provide the album model."""
from typing import Dict, List

from .copyright import Copyright
from .image import Image
from .paging import Paging
from .simplified_artist import SimplifiedArtist
from .simplified_track import SimplifiedTrack


class Album:
    """An album."""

    def __init__(self, data):
        self._album_type = data["album_type"]
        self._artists = [SimplifiedArtist(d) for d in data["artists"]]
        self._available_markets = data["available_markets"]
        self._copyrights = [Copyright(d) for d in data["copyrights"]]
        self._external_ids = data["external_ids"]
        self._external_urls = data["external_urls"]
        self._genres = data["genres"]
        self._href = data["href"]
        self._id = data["id"]
        self._images = [Image(d) for d in data["images"]]
        self._label = data["label"]
        self._name = data["name"]
        self._popularity = data["popularity"]
        self._release_date = data["release_date"]
        self._release_date_precision = data["release_date_precision"]
        self._tracks = Paging(data["tracks"], SimplifiedTrack)
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
    def available_markets(self) -> List[str]:
        """
        The markets in which the album is available: ISO 3166-1 alpha-2 country codes. Note that an album is considered
        available in a market when at least 1 of its tracks is available in that market.
        """
        return self._available_markets

    @property
    def copyrights(self) -> List[Copyright]:
        """The copyright statements of the album."""
        return self._copyrights

    @property
    def external_ids(self) -> Dict[str, str]:
        """Known external IDs for the album."""
        return self._external_ids

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this album."""
        return self._external_urls

    @property
    def genres(self) -> List[str]:
        """A list of the genres used to classify the album. For example: "Prog Rock" , "Post-Grunge"."""
        return self._genres

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
    def label(self) -> str:
        """The label for the album."""
        return self._label

    @property
    def name(self) -> str:
        """The name of the album. In case of an album takedown, the value may be an empty string."""
        return self._name

    @property
    def popularity(self) -> int:
        """
        The popularity of the album. The value will be between 0 and 100, with 100 being the most popular. The
        popularity is calculated from the popularity of the album’s individual tracks.
        """
        return self._popularity

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
    def tracks(self) -> Paging:
        """The tracks of the album."""
        return self._tracks

    @property
    def type(self) -> str:
        """The object type: “album”"""
        return self._type

    @property
    def uri(self) -> str:
        """The Spotify URI for the album."""
        return self._uri
