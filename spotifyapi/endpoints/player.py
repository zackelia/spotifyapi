"""Provide the player endpoint."""
from typing import List, Generator, Optional

from .base import EndpointBase
from ..models.currently_playing import CurrentlyPlaying, CurrentlyPlayingContext
from ..models.device import Device
from ..models.paging import Paging
from ..models.play_history import PlayHistory


class PlayerEndpoint(EndpointBase):
    """Retrieve and modify the user's playback."""

    def __init__(self, access_token: str):
        super().__init__(access_token)

        self._url += "/me/player"

    def get_devices(self) -> List[Device]:
        """Get information about a user’s available devices.

        Returns: A list of devices
        """
        response = self._get(f"{self._url}/devices")

        return [Device(data) for data in response.json()["devices"]]

    def get_playback(self) -> CurrentlyPlayingContext:
        """Get information about the user’s current playback state, including track, track progress, and active device.

        Returns:
            Current playback information.
        """
        response = self._get(f"{self._url}")

        return CurrentlyPlayingContext(response.json())

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

        Yields:
            A play history.
        """
        # If limit is specified, check that it is a legitimate value
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        # After and before are mutually exclusive
        if after and before:
            raise ValueError("Can only specify after or before, not both")

        params = {"limit": limit, "after": after, "before": before}

        response = self._get(f"{self._url}/recently-played", params=params)

        paging = Paging(response.json(), PlayHistory)

        # Yield all play history objects
        while True:
            for item in paging.items:
                yield item

            if not paging.next:
                break

            response = self._get(paging.next)
            paging = Paging(response.json(), PlayHistory)

    def get_currently_playing_track(self) -> CurrentlyPlaying:
        """Get the object currently being played on the user’s Spotify account.

        Returns:
            Currently playing object information.
        """
        response = self._get(f"{self._url}/currently-playing")

        return CurrentlyPlaying(response.json())

    def pause(self, device_id: Optional[str] = None) -> None:
        """Pause playback on the user’s account.

        Args:
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.
        """
        params = {"device_id": device_id}

        self._put(f"{self._url}/pause", params=params)

    def seek(self, position_ms: int, device_id: Optional[str] = None) -> None:
        """Seeks to the given position in the user’s currently playing track.

        Args:
            position_ms: The position in milliseconds to seek to. Must be a positive number. Passing in a position that
                is greater than the length of the track will cause the player to start playing the next song.
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.

        Raises:
            ValueError: If `position_ms` is not a positive value
        """
        if position_ms < 0:
            raise ValueError("position_ms must be a positive value")

        params = {"position_ms": position_ms, "device_id": device_id}

        self._put(f"{self._url}/seek", params=params)

    def repeat(self, state: str, device_id: Optional[str] = None) -> None:
        """Set the repeat mode for the user’s playback. Options are repeat-track, repeat-context, and off.

        Args:
            state: track, context or off.
                track will repeat the current track.
                context will repeat the current context.
                off will turn repeat off.
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.

        Raises:
            ValueError: If `state` is not a valid option
        """
        if state not in ["track", "context", "off"]:
            raise ValueError("state must be track, context, or off")

        params = {"state": state, "device_id": device_id}

        self._put(f"{self._url}/repeat", params=params)

    def volume(self, volume_percent: int, device_id: Optional[str] = None) -> None:
        """Set the volume for the user’s current playback device.

        Args:
            volume_percent: The volume to set. Must be a value from 0 to 100 inclusive.
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.

        Raises:
            ValueError: If `volume_percent` is not between 0 and 100
        """
        if not 0 <= volume_percent <= 100:
            raise ValueError("volume_percent must be between 0 and 100")

        params = {"volume_percent": volume_percent, "device_id": device_id}

        self._put(f"{self._url}/volume", params=params)

    def next(self, device_id: Optional[str] = None) -> None:
        """Skips to next track in the user’s queue.

        Args:
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
            device is the target.
        """
        params = {"device_id": device_id}

        self._post(f"{self._url}/next", params=params)

    def previous(self, device_id: Optional[str] = None) -> None:
        """Skips to previous track in the user’s queue.

        Args:
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.
        """
        params = {"device_id": device_id}

        self._post(f"{self._url}/previous", params=params)

    def play(self, device_id: Optional[str] = None) -> None:
        """Start a new context or resume current playback on the user’s active device.

        Args:
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.
        """
        params = {"device_id": device_id}

        self._put(f"{self._url}/play", params=params)

    def shuffle(self, state: bool, device_id: Optional[str] = None) -> None:
        """Toggle shuffle on or off for user’s playback.

        Args:
            state:
                True : Shuffle user’s playback
                False : Do not shuffle user’s playback.
            device_id: The id of the device this command is targeting. If not supplied, the user’s currently active
                device is the target.
        """
        params = {"state": state, "device_id": device_id}

        self._put(f"{self._url}/shuffle", params=params)

    def transfer_playback(self, device: Device, play: Optional[bool] = None) -> None:
        """Transfer playback to a new device and determine if it should start playing.

        Args:
            device: The device on which playback should be started/transferred.
            play:
                True: ensure playback happens on new device.
                False/None: keep the current playback state.
        """
        data = {"device_ids": [device.id], "play": play}

        self._put(f"{self._url}", data=data)
