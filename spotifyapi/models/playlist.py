"""Provide the playlist model."""
from typing import Dict, List, Optional

from .image import Image
from .public_user import PublicUser
from .tracks import Tracks


class Playlist:
    """A playlist."""

    def __init__(self, data):
        self._collaborative = data["collaborative"]
        self._external_urls = data["external_urls"]
        self._href = data["href"]
        self._id = data["id"]
        self._images = [Image(d) for d in data["images"]]
        self._name = data["name"]
        self._owner = PublicUser(data["owner"])
        self._public = data["public"]
        self._snapshot_id = data["snapshot_id"]
        self._tracks = Tracks(data["tracks"])
        self._uri = data["uri"]

    @property
    def collaborative(self) -> bool:
        """
        Returns true if context is not search and the owner allows other users to modify the playlist. Otherwise returns
        false.
        """
        return self._collaborative

    @property
    def external_urls(self) -> Dict[str, str]:
        """Known external URLs for this playlist."""
        return self._external_urls

    @property
    def href(self) -> str:
        """A link to the Web API endpoint providing full details of the playlist."""
        return self._href

    @property
    def id(self) -> str:
        """The Spotify ID for the playlist."""
        return self._id

    @property
    def images(self) -> List[Optional[Image]]:
        """
        Images for the playlist. The array may be empty or contain up to three images. The images are returned by size
        in descending order. See https://developer.spotify.com/documentation/general/guides/working-with-playlists/.

        Note: If returned, the source URL for the image is temporary and will expire in less than a day.
        """
        return self._images

    @property
    def name(self) -> str:
        """The name of the playlist."""
        return self._name

    @property
    def owner(self) -> PublicUser:
        """The user who owns the playlist"""
        return self._owner

    @property
    def public(self) -> Optional[bool]:
        """
        The playlist’s public/private status: true the playlist is public, false the playlist is private, None the
        playlist status is not relevant. For more about public/private status, see
        https://developer.spotify.com/documentation/general/guides/working-with-playlists/.
        """
        return self._public

    @property
    def snapshot_id(self) -> str:
        """
        The version identifier for the current playlist. Can be supplied in other requests to target a specific playlist
        version.
        """
        return self._snapshot_id

    @property
    def tracks(self) -> Tracks:
        """
        A collection containing a link to the Web API endpoint where full details of the playlist’s tracks can be
        retrieved, along with the total number of tracks in the playlist.
        """
        return self._tracks

    @property
    def uri(self) -> str:
        """The Spotify URI for the playlist."""
        return self._uri
