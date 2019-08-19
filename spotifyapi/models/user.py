"""Provide the user model."""
from typing import Dict, List, Optional

from .followers import Followers
from .image import Image


class User:
    """A User."""

    def __init__(self, data):
        self._display_name = data["display_name"] if 'display_name' in data else None
        self._external_urls = data["external_urls"]
        self._followers = data["followers"]
        self._href = data["href"]
        self._id = data["id"]
        self._images = data["images"]
        self._type = data["type"]
        self._uri = data["uri"]

    @property
    def display_name(self) -> Optional[str]:
        """The name displayed on the user’s profile."""
        return self._display_name

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this artist."""
        return self._external_urls

    @property
    def followers(self) -> Followers:
        """Information about the followers of this user."""
        return self._followers

    @property
    def href(self) -> str:
        """A link to the Web API endpoint for this user."""
        return self._href

    @property
    def id(self) -> str:
        """The Spotify user ID for this user."""
        return self._id

    @property
    def images(self) -> List[Image]:
        """The user’s profile image."""
        return self._images

    @property
    def type(self) -> str:
        """The object type: “user”."""
        return self._type

    @property
    def uri(self) -> str:
        """The Spotify URI for this user."""
        return self._uri
