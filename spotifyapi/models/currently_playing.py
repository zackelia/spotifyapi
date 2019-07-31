"""Provide the currently playing model."""
from typing import Optional

from .context import Context
from .device import Device
from .full_track import FullTrack


class CurrentlyPlaying:
    """Information about the currently playing track."""

    def __init__(self, data):
        self._context = Context(data["context"])
        self._timestamp = data["timestamp"]
        self._progress_ms = data["progress_ms"]
        self._is_playing = data["is_playing"]
        self._item = FullTrack(data["item"])
        self._currently_playing_type = data["currently_playing_type"]

    @property
    def context(self) -> Optional[Context]:
        """A Context Object. Can be None."""
        return self._context

    @property
    def timestamp(self) -> int:
        """Unix Millisecond Timestamp when data was fetched."""
        return self._timestamp

    @property
    def progress_ms(self) -> Optional[int]:
        """Progress into the currently playing track. Can be None."""
        return self._progress_ms

    @property
    def is_playing(self) -> bool:
        """If something is currently playing."""
        return self._is_playing

    @property
    def item(self) -> Optional[FullTrack]:
        """The currently playing track. Can be None."""
        return self._item

    @property
    def currently_playing_type(self) -> str:
        """The object type of the currently playing item. Can be one of track, episode, ad or unknown."""
        return self._currently_playing_type


class CurrentlyPlayingContext(CurrentlyPlaying):
    """Information about the currently playing track."""

    def __init__(self, data):
        super().__init__(data)

        self._device = Device(data["device"])
        self._repeat_state = data["repeat_state"]
        self._shuffle_state = data["shuffle_state"]

    @property
    def device(self) -> Device:
        """The device that is currently active."""
        return self._device

    @property
    def repeat_state(self) -> str:
        """off, track, context."""
        return self._repeat_state

    @property
    def shuffle_state(self) -> bool:
        """If shuffle is on or off."""
        return self._shuffle_state
