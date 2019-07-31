"""Provides the play history module."""
from .context import Context
from .simplified_track import SimplifiedTrack


class PlayHistory:
    """A previously played track."""

    def __init__(self, data):
        self._track = SimplifiedTrack(data["track"])
        self._played_at = data["played_at"]
        self._context = Context(data["context"])

    @property
    def track(self) -> SimplifiedTrack:
        """The track the user listened to."""
        return self._track

    @property
    def played_at(self) -> str:
        """The date and time the track was played."""
        return self._played_at

    @property
    def context(self) -> Context:
        """The context the track was played from."""
        return self._context
