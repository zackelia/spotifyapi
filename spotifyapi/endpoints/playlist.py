"""Provide the playlist endpoint."""
import base64
from typing import Generator, List, Optional, Union
from requests_oauthlib import OAuth2Session

from .base import EndpointBase
from ..authorization.decorators import scope
from ..authorization.scopes import (
    playlist_read_private,
    playlist_modify_private,
    playlist_modify_public,
    playlist_read_collaborative,
    ugc_image_upload,
)
from ..models import (
    FullPlaylist,
    Image,
    Paging,
    Playlist,
    PlaylistTrack,
    PrivateUser,
    SimplifiedPlaylist,
    Track,
    User,
)
from ..utils import generate


class PlaylistEndpoint(EndpointBase):
    """Endpoints for retrieving information about a user’s playlists and for managing a user’s playlists."""

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)

    @scope(playlist_modify_public, playlist_modify_private)
    def add_playlist_tracks(
        self,
        playlist: Playlist,
        tracks: Union[Track, List[Track]],
        position: Optional[int] = None,
    ) -> str:
        """Add one or more tracks to a user’s playlist.

        Args:
            playlist: The playlist to add to.
            tracks: The track or tracks to add.
            position: The position to insert the tracks, a zero-based index. For example, to insert the tracks in the
                first position: position=0; to insert the tracks in the third position: position=2 . If omitted, the
                tracks will be appended to the playlist. Tracks are added in the order they are listed in the query
                string or request body.

        Returns:
            The snapshot_id that can be used to identify your playlist version in future requests.

        Raises:
            ValueError: If more than 100 tracks are provided.
        """
        if isinstance(tracks, list) and len(tracks) > 100:
            raise ValueError("Can only add 100 tracks at a time")

        data = {"position": position}

        if isinstance(tracks, Track):
            data["uris"] = [tracks.uri]
        else:
            data["uris"] = [track.uri for track in tracks]

        response = self._post(
            f"{self._base_url}/playlists/{playlist.id}/tracks", data=data
        )

        return response.json()["snapshot_id"]

    @scope(playlist_modify_public, playlist_modify_private)
    def change_playlist_details(
        self,
        playlist: Playlist,
        name: Optional[str] = None,
        public: Optional[bool] = None,
        collaborative: Optional[bool] = None,
        description: Optional[str] = None,
    ):
        """Change a playlist’s name and public/private state. (The user must, of course, own the playlist.)

        Args:
            playlist: The playlist to change.
            name: The new name for the playlist, for example "My New Playlist Title".
            public: If true the playlist will be public, if false it will be private.
            collaborative: If true , the playlist will become collaborative and other users will be able to modify the
                playlist in their Spotify client. Note: You can only set collaborative to true on non-public playlists.
            description: Value for playlist description as displayed in Spotify Clients and in the Web API.

        Raises:
            ValueError: If the playlist is set as collaborative and private. If a description is not provided and the
                playlist is SimplifiedPlaylist.
        """
        if collaborative and public:
            raise ValueError("Collaborative playlists can only be private")

        if isinstance(playlist, SimplifiedPlaylist):
            raise ValueError(
                "Must provide either full playlist or provide a description"
            )

        data = {
            "name": name if name else playlist.name,
            "public": public if public else playlist.public,
            "collaborative": collaborative if collaborative else playlist.collaborative,
            "description": description if description else playlist.description,
        }

        self._put(f"{self._base_url}/playlists/{playlist.id}", data=data)

    @scope(playlist_modify_public, playlist_modify_private)
    def create_playlist(
        self,
        name: str,
        public: Optional[bool] = True,
        collaborative: Optional[bool] = False,
        description: Optional[str] = None,
    ) -> FullPlaylist:
        """Create a playlist for a Spotify user. (The playlist will be empty until you add tracks.)

        Args:
            name: The name for the new playlist, for example "Your Coolest Playlist" . This name does not need to be
                unique; a user may have several playlists with the same name.
            public: Defaults to true . If true the playlist will be public, if false it will be private. To be able to
                create private playlists, the user must have granted the playlist-modify-private scope.
            collaborative: Defaults to false . If true the playlist will be collaborative. Note that to create a
                collaborative playlist you must also set public to false . To create collaborative playlists you must
                have granted playlist-modify-private and playlist-modify-public scopes.
            description: value for playlist description as displayed in Spotify Clients and in the Web API.

        Returns:
            The playlist just created.

        Raises:
            ValueError: If the playlist is set as collaborative and private.
        """
        if collaborative and public:
            raise ValueError("Collaborative playlists can only be private")

        # Get the current user, apparently the Spotify API doesn't do that for you?
        response = self._get(f"{self._base_url}/me")

        me = PrivateUser(response.json())

        data = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description,
        }

        response = self._post(f"{self._base_url}/users/{me.id}/playlists", data=data)

        return FullPlaylist(response.json(), self._oauth)

    @scope(playlist_read_private)
    def get_current_playlists(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Generator[SimplifiedPlaylist, None, None]:
        """Get a generator of the playlists owned or followed by the current Spotify user.

        Args:
            limit: The maximum number of playlists to return. Default: 20. Minimum: 1. Maximum: 50.
            offset: The index of the first playlist to return. Default: 0 (the first object). Maximum offset: 100,000.
                Use with limit to get the next set of playlists.

        Returns:
            A generator of the user's playlists.

        Raises:
            ValueError: If limit is outside [1, 50]. If offset is used without limit. If offset is > 100,000.
        """
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        if offset and offset > 100_000:
            raise ValueError("offset must be 100,000 or below")

        params = {"limit": limit, "offset": offset}

        response = self._get(f"{self._base_url}/me/playlists", params=params)

        paging = Paging(response.json(), SimplifiedPlaylist)

        return generate(paging, self._oauth)

    @scope(playlist_modify_private, playlist_read_collaborative)
    def get_users_playlists(
        self, user: User, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Generator[SimplifiedPlaylist, None, None]:
        """Get a generator of the playlists owned or followed by a Spotify user.

        Args:
            user: The user to get playlists from.
            limit: The maximum number of playlists to return. Default: 20. Minimum: 1. Maximum: 50.
            offset: The index of the first playlist to return. Default: 0 (the first object). Maximum offset: 100,000.
                Use with limit to get the next set of playlists.

        Returns:
            A generator of the user's playlists.

        Raises:
            ValueError: If limit is outside [1, 50]. If offset is used without limit. If offset is > 100,000.
        """
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        if offset and offset > 100_000:
            raise ValueError("offset must be 100,000 or below")

        params = {"limit": limit, "offset": offset}

        response = self._get(
            f"{self._base_url}/users/{user.id}/playlists", params=params
        )

        paging = Paging(response.json(), SimplifiedPlaylist)

        return generate(paging, self._oauth)

    def get_playlist_cover_image(self, playlist: Playlist) -> Union[Image, List[Image]]:
        """Get the current image(s) associated with a specific playlist.

        Args:
            playlist: The playlist to get the cover image of.

        Returns:
            An image or list of images.
        """
        response = self._get(f"{self._base_url}/playlists/{playlist.id}/images")

        images = [Image(data) for data in response.json()]

        if len(images) == 1:
            return images[0]
        else:
            return images

    def get_playlist(self, id: str) -> FullPlaylist:
        """Get a playlist owned by a Spotify user.

        Args:
            id: The ID of the playlist.

        Returns:
            A playlist.
        """
        response = self._get(f"{self._base_url}/playlists/{id}")

        return FullPlaylist(response.json(), self._oauth)

    def get_playlist_tracks(
        self,
        playlist: Playlist,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Generator[PlaylistTrack, None, None]:
        """Get full details of the tracks of a playlist owned by a Spotify user.

        Args:
            playlist: The playlist to get tracks for.
            limit: The maximum number of playlists to return. Default: 20. Minimum: 1. Maximum: 50.
            offset: The index of the first playlist to return. Default: 0 (the first object). Use with limit to get the
                next set of playlists.

        Returns:
            A generator of the playlist's tracks.

        Raises:
            ValueError: If limit is outside [1, 50]. If offset is used without limit.
        """
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        response = self._get(f"{self._base_url}/playlists/{playlist.id}/tracks")

        paging = Paging(response.json(), PlaylistTrack)

        return generate(paging, self._oauth)

    @scope(playlist_modify_public, playlist_modify_private)
    def remove_playlist_tracks(
        self, playlist: Playlist, tracks: Union[Track, List[Track]]
    ) -> str:
        """Remove one or more tracks from a user’s playlist.

        Args:
            playlist: The playlist to remove from.
            tracks: The track or tracks to remove.

        Returns:
            The snapshot ID of the playlist.

        Raises:
            ValueError: If more than 100 tracks are provided.
        """
        if isinstance(tracks, list) and len(tracks) > 100:
            raise ValueError("Can only remove 100 tracks at a time")

        data = {}

        if isinstance(tracks, Track):
            data["tracks"] = [{"uri": tracks.uri}]
        else:
            data["tracks"] = [{"uri": track.uri} for track in tracks]

        response = self._delete(
            f"{self._base_url}/playlists/{playlist.id}/tracks", data=data
        )

        return response.json()["snapshot_id"]

    @scope(playlist_modify_public, playlist_modify_private)
    def reorder_playlist_tracks(
        self,
        playlist: Playlist,
        start: int,
        insert_before: int,
        length: Optional[int] = None,
        snapshot_id: Optional[str] = None,
    ) -> str:
        """Reorder a track or a group of tracks in a playlist.

        When reordering tracks, the timestamp indicating when they were added and the user who added them will be kept
        untouched. In addition, the users following the playlists won’t be notified about changes in the playlists when
        the tracks are reordered.

        Args:
            playlist: The playlist to reorder.
            start: The start index to move.
            insert_before: The index to move the track(s) to.
            length: The number of tracks to move.
            snapshot_id: A snapshot ID.

        Returns:
            A snapshot ID.
        """
        data = {
            "range_start": start,
            "insert_before": insert_before,
            "range_length": length,
            "snapshot_id": snapshot_id,
        }

        response = self._put(
            f"{self._base_url}/playlists/{playlist.id}/tracks", data=data
        )

        return response.json()["snapshot_id"]

    @scope(playlist_modify_public, playlist_modify_private)
    def replace_playlist_tracks(
        self, playlist: Playlist, tracks: Union[Track, List[Track]]
    ):
        """Replace all the tracks in a playlist, overwriting its existing tracks. This powerful request can be useful
            for replacing tracks, re-ordering existing tracks, or clearing the playlist.

        Args:
            playlist: The playlist to replace tracks.
            tracks: The tracks to replace with.

        Raises:
            ValueError: If more than 100 tracks are provided.
        """
        if isinstance(tracks, list) and len(tracks) > 100:
            raise ValueError("Can only replace 100 tracks at a time")

        data = {}

        if isinstance(tracks, Track):
            data["uris"] = [tracks.uri]
        else:
            data["uris"] = [track.uri for track in tracks]

        self._put(f"{self._base_url}/playlists/{playlist.id}/tracks", data=data)

    @scope(ugc_image_upload, playlist_modify_public, playlist_modify_private)
    def upload_playlist_cover_image(self, playlist: Playlist, image_path: str):
        """Replace the image used to represent a specific playlist.

        Args:
            playlist: The playlist to add the image to.
            image_path: The path to the JPG image.
        """
        with open(image_path, "rb") as image:
            image_data = image.read()
            image_data_encoded = base64.b64encode(image_data)

        headers = {"Content-type": "image/jpeg"}

        self._oauth.put(
            f"{self._base_url}/playlists/{playlist.id}/images",
            data=image_data_encoded,
            headers=headers,
        )
