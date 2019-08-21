"""Provide the playlist track model."""
from typing import Optional

from .full_track import FullTrack
from .public_user import PublicUser


class PlaylistTrack:
    """Information about the tracks of the playlist."""

    def __init__(self, data):
        self._added_at = data["added_at"]
        self._added_by = PublicUser(data["added_by"]) if data["added_by"] else None
        self._is_local = data["is_local"]
        self._primary_color = data["primary_color"]
        self._track = FullTrack(data["track"])
        self._video_thumbnail = data["video_thumbnail"]["url"]

    @property
    def added_at(self) -> Optional[str]:
        """The date and time the track was added. Note that some very old playlists may return null in this field."""
        return self._added_at

    @property
    def added_by(self) -> Optional[PublicUser]:
        """The Spotify user who added the track. Note that some very old playlists may return null in this field."""
        return self._added_by

    @property
    def is_local(self) -> bool:
        """Whether this track is a local file or not."""
        return self._is_local

    @property
    def primary_color(self) -> str:
        """Undocumented, appears to be unused."""
        return self._primary_color

    @property
    def track(self) -> FullTrack:
        """Information about the track."""
        return self._track

    @property
    def video_thumbnail(self) -> Optional[str]:
        """Undocumented, appears to be unused."""
        return self._video_thumbnail
