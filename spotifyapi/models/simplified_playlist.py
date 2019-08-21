"""Provide the simplified playlist model."""
from .playlist import Playlist


class SimplifiedPlaylist(Playlist):
    """A simplified playlist. This is the same as Playlist but matches the Spotify API naming scheme."""

    def __init__(self, data):
        super().__init__(data)
