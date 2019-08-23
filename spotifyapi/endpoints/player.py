"""Provide the player endpoint."""
from typing import List, Generator, Optional
from requests_oauthlib import OAuth2Session

from .base import EndpointBase
from ..authorization.decorators import scope
from ..authorization.scopes import (
    user_modify_playback_state,
    user_read_currently_playing,
    user_read_playback_state,
    user_read_recently_played,
)
from ..models import CurrentlyPlaying, CurrentlyPlayingContext, Device, PlayHistory
from ..utils import generate


class PlayerEndpoint(EndpointBase):
    """Retrieve and modify the user's playback."""

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)

        self._player = f"{self._base_url}/me/player"

    @scope(user_read_playback_state)
    def get_devices(self) -> List[Device]:
        """Get information about a user’s available devices.

        Returns: A list of devices
        """
        response = self._get(f"{self._player}/devices")

        return [Device(data) for data in response.json()["devices"]]

    @scope(user_read_playback_state)
    def get_playback(self) -> Optional[CurrentlyPlayingContext]:
        """Get information about the user’s current playback state, including track, track progress, and active device.

        The information returned is for the last known state, which means an inactive device could be returned if it was
        the last one to execute playback. When no available devices are found, None is returned.

        Returns:
            Current playback information.
        """
        response = self._get(f"{self._player}")

        if response:
            return CurrentlyPlayingContext(response.json())

    @scope(user_read_recently_played)
    def get_recently_played_tracks(
        self,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> Generator[PlayHistory, None, None]:
        """Get tracks from the current user’s recently played tracks.

        Args:
            limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
            after: A Unix timestamp in milliseconds. Returns all items after (but not including) this cursor position.
                If after is specified, before must not be specified.
            before: A Unix timestamp in milliseconds. Returns all items before (but not including) this cursor position.
                If before is specified, after must not be specified.

        Raises:
            ValueError:
                If specified `limit` is outside the valid range
                If both `after` and `before` are specified

        Returns:
            A generator of play histories.
        """
        # If limit is specified, check that it is a legitimate value
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        # After and before are mutually exclusive
        if after and before:
            raise ValueError("Can only specify after or before, not both")

        params = {"limit": limit, "after": after, "before": before}

        response = self._get(f"{self._player}/recently-played", params=params)

        return generate(response.json(), PlayHistory, self._oauth)

    @scope(user_read_currently_playing, user_read_playback_state)
    def get_currently_playing(self) -> Optional[CurrentlyPlaying]:
        """Get the object currently being played on the user’s Spotify account.

        The information returned is for the last known state, which means an inactive device could be returned if it was
        the last one to execute playback. When no available devices are found, None is returned. If private session is
        enabled, None is returned.

        Returns:
            Currently playing object information.
        """
        response = self._get(f"{self._player}/currently-playing")

        if response:
            return CurrentlyPlaying(response.json())

    @scope(user_modify_playback_state)
    def pause(self, device: Optional[Device] = None) -> None:
        """Pause playback on the user’s account.

        Args:
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.
        """
        params = {}

        if device:
            params["device_id"] = device.id

        self._put(f"{self._player}/pause", params=params)

    @scope(user_modify_playback_state)
    def seek(self, position_ms: int, device: Optional[Device] = None) -> None:
        """Seeks to the given position in the user’s currently playing track.

        Args:
            position_ms: The position in milliseconds to seek to. Must be a positive number. Passing in a position that
                is greater than the length of the track will cause the player to start playing the next song.
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.

        Raises:
            ValueError: If `position_ms` is not a positive value
        """
        if position_ms < 0:
            raise ValueError("position_ms must be a positive value")

        params = {"position_ms": position_ms}

        if device:
            params["device"] = device.id

        self._put(f"{self._player}/seek", params=params)

    @scope(user_modify_playback_state)
    def repeat(self, state: str, device: Optional[Device] = None) -> None:
        """Set the repeat mode for the user’s playback. Options are repeat-track, repeat-context, and off.

        Args:
            state: track, context or off.
                track will repeat the current track.
                context will repeat the current context.
                off will turn repeat off.
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.

        Raises:
            ValueError: If `state` is not a valid option
        """
        if state not in ["track", "context", "off"]:
            raise ValueError("state must be track, context, or off")

        params = {"state": state}

        if device:
            params["device_id"] = device.id

        self._put(f"{self._player}/repeat", params=params)

    @scope(user_modify_playback_state)
    def volume(self, volume_percent: int, device: Optional[Device] = None) -> None:
        """Set the volume for the user’s current playback device.

        Args:
            volume_percent: The volume to set. Must be a value from 0 to 100 inclusive.
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.

        Raises:
            ValueError: If `volume_percent` is not between 0 and 100
        """
        if not 0 <= volume_percent <= 100:
            raise ValueError("volume_percent must be between 0 and 100")

        params = {"volume_percent": volume_percent}

        if device:
            params["device_id"] = device.id

        self._put(f"{self._player}/volume", params=params)

    @scope(user_modify_playback_state)
    def next(self, device: Optional[Device] = None) -> None:
        """Skips to next track in the user’s queue.

        Args:
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.
        """
        params = {}

        if device:
            params["device_id"] = device.id

        self._post(f"{self._player}/next", params=params)

    @scope(user_modify_playback_state)
    def previous(self, device: Optional[Device] = None) -> None:
        """Skips to previous track in the user’s queue.

        Args:
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.
        """
        params = {}

        if device:
            params["device_id"] = device.id

        self._post(f"{self._player}/previous", params=params)

    @scope(user_modify_playback_state)
    def play(self, device: Optional[Device] = None) -> None:
        """Start a new context or resume current playback on the user’s active device.

        Args:
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.
        """
        params = {}

        if device:
            params["device_id"] = device.id

        self._put(f"{self._player}/play", params=params)

    @scope(user_modify_playback_state)
    def shuffle(self, state: bool, device: Optional[Device] = None) -> None:
        """Toggle shuffle on or off for user’s playback.

        Args:
            state:
                True : Shuffle user’s playback
                False : Do not shuffle user’s playback.
            device: The device this command is targeting. If not supplied, the user’s currently active device is the
                target.
        """
        params = {"state": state}

        if device:
            params["device_id"] = device.id

        self._put(f"{self._player}/shuffle", params=params)

    @scope(user_modify_playback_state)
    def transfer_playback(self, device: Device, play: Optional[bool] = None) -> None:
        """Transfer playback to a new device and determine if it should start playing.

        Args:
            device: The device on which playback should be started/transferred.
            play:
                True: ensure playback happens on new device.
                False/None: keep the current playback state.
        """
        data = {"device_ids": [device.id], "play": play}

        self._put(f"{self._player}", data=data)
