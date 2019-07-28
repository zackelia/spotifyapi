"""Provide the device module."""
from typing import Optional


class Device:
    """Any device."""

    def __init__(self, data):
        self._id = data["id"]
        self._is_active = data["is_active"]
        self._is_private_session = data["is_private_session"]
        self._is_restricted = data["is_restricted"]
        self._name = data["name"]
        self._type = data["type"]
        self._volume_percent = data["volume_percent"]

    @property
    def id(self) -> Optional[str]:
        """The device ID. This may be None."""
        return self._id

    @property
    def is_active(self) -> bool:
        """If this device is the currently active device."""
        return self._is_active

    @property
    def is_private_session(self) -> bool:
        """If this device is currently in a private session."""
        return self._is_private_session

    @property
    def is_restricted(self) -> bool:
        """
        Whether controlling this device is restricted. At present if this is “true” then no Web API commands will be
        accepted by this device.
        """
        return self._is_restricted

    @property
    def name(self) -> str:
        """The name of the device."""
        return self._name

    @property
    def type(self) -> str:
        """Device type, such as “computer”, “smartphone” or “speaker”."""
        return self._type

    @property
    def volume_percent(self) -> Optional[int]:
        """The current volume in percent. This may be None."""
        return self._volume_percent
