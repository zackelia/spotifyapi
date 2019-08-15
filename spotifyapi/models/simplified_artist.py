"""Provide the simplified artist model."""
from .artist import Artist


class SimplifiedArtist(Artist):
    """A simplified artist. This is the same as Artist but matches the Spotify API naming scheme."""

    def __init__(self, data):
        super().__init__(data)
