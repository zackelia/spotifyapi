"""Provide the full track module."""
from typing import Dict, List, Optional

from .album import Album
from .simplified_artist import SimplifiedArtist


class FullTrack:
    """A full track."""

    def __init__(self, data):
        self._album = Album(data["album"])
        self._artists = [SimplifiedArtist(d) for d in data["artists"]]
        self._available_markets = data["available_markets"]
        self._disc_number = data["disc_number"]
        self._duration_ms = data["duration_ms"]
        self._explicit = data["explicit"]
        self._external_ids = data["external_ids"]
        self._external_urls = data["external_urls"]
        self._href = data["href"]
        self._id = data["id"]
        self._is_local = data["is_local"]
        self._name = data["name"]
        self._popularity = data["popularity"]
        self._preview_url = data["preview_url"]
        self._track_number = data["track_number"]
        self._type = data["type"]
        self._uri = data["uri"]

    @property
    def album(self) -> Album:
        """
        The album on which the track appears. The album object includes a link in href to full information about the
        album.
        """
        return self._album

    @property
    def artists(self) -> List[SimplifiedArtist]:
        """
        The artists who performed the track. Each artist object includes a link in href to more detailed information
        about the artist.
        """
        return self._artists

    @property
    def available_markets(self) -> List[str]:
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
    def external_ids(self) -> Dict[str, str]:
        """Known external IDs for the track."""
        return self._external_ids

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this track."""
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
    def popularity(self) -> int:
        """
        The popularity of the track. The value will be between 0 and 100, with 100 being the most popular.

        The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is
        calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how
        recent those plays are.

        Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were
        played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated
        independently. Artist and album popularity is derived mathematically from track popularity. Note that the
        popularity value may lag actual popularity by a few days: the value is not updated in real time.
        """
        return self._popularity

    @property
    def preview_url(self) -> Optional[str]:
        """A link to a 30 second preview (MP3 format) of the track. Can be None."""
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
