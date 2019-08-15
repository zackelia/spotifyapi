"""Provide the simplified album model."""
from .album import Album


class SimplifiedAlbum(Album):
    """A simplified album. This is the same as Album but matches the Spotify API naming scheme."""

    def __init__(self, data):
        super().__init__(data)
