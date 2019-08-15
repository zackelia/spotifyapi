"""Provide the saved album model."""
from .full_album import FullAlbum


class SavedAlbum:
    """A saved album."""

    def __init__(self, data):
        self._added_at = data["added_at"]
        self._album = FullAlbum(data["album"])

    @property
    def added_at(self) -> str:
        """The date and time the album was saved."""
        return self._added_at

    @property
    def album(self) -> FullAlbum:
        """Information about the album."""
        return self._album
