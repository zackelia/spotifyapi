"""Provide the saved track model."""
from .full_track import FullTrack


class SavedTrack:
    """A saved track."""

    def __init__(self, data):
        self._added_at = data["added_at"]
        self._track = FullTrack(data["track"])

    @property
    def added_at(self) -> str:
        """The date and time the track was saved."""
        return self._added_at

    @property
    def track(self) -> FullTrack:
        """Information about the track."""
        return self._track
