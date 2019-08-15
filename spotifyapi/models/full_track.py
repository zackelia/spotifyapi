"""Provide the full track model."""
from typing import Dict

from .simplified_album import SimplifiedAlbum
from .track import Track


class FullTrack(Track):
    """A full track."""

    def __init__(self, data):
        super().__init__(data)

        self._album = SimplifiedAlbum(data["album"])
        self._external_ids = data["external_ids"]
        self._popularity = data["popularity"]

    @property
    def album(self) -> SimplifiedAlbum:
        """
        The album on which the track appears. The album object includes a link in href to full information about the
        album.
        """
        return self._album

    @property
    def external_ids(self) -> Dict[str, str]:
        """Known external IDs for the track."""
        return self._external_ids

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
