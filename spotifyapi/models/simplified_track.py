"""Provide the simplified track model."""
from .track import Track


class SimplifiedTrack(Track):
    """A simplified track. This is the same as Track but matches the Spotify API naming scheme."""

    def __init__(self, data):
        super().__init__(data)
