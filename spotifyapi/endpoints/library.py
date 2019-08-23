"""Provide the user library endpoint."""
from typing import Generator, List, Optional, Union
from requests_oauthlib import OAuth2Session

from .base import EndpointBase
from ..authorization.decorators import scope
from ..authorization.scopes import user_library_read, user_library_modify
from ..models import Album, SavedAlbum, SavedTrack, Track
from ..utils import generate


class LibraryEndpoint(EndpointBase):
    """
    Endpoints for retrieving information about, and managing, tracks that the current user has saved in their “Your
    Music” library.
    """

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)

        self._library = f"{self._base_url}/me"

    @scope(user_library_read)
    def is_album_saved(
        self, albums: Union[Album, List[Album]]
    ) -> Union[bool, List[bool]]:
        """Check if one or more albums is already saved in the current Spotify user’s ‘Your Music’ library.

        Args:
            albums: The album or albums to check.

        Raises:
            ValueError: If more than 50 albums are provided.

        Returns:
            True/False for one album or a list of True/False for multiple albums.
        """
        if isinstance(albums, list):
            if len(albums) > 50:
                raise ValueError("Maximum albums to check is 50")

            params = {"ids": ",".join([item.id for item in albums])}

        else:
            params = {"ids": albums.id}

        response = self._get(f"{self._library}/albums/contains", params=params)

        return response.json()[0] if len(response.json()) == 1 else response.json()

    @scope(user_library_read)
    def is_track_saved(
        self, tracks: Union[Track, List[Track]]
    ) -> Union[bool, List[bool]]:
        """Check if one or more tracks is already saved in the current Spotify user’s ‘Your Music’ library.

        Args:
            tracks: The track or tracks to check.

        Raises:
            ValueError: If more than 50 tracks are provided.

        Returns:
            True/False for one track or a list of True/False for multiple tracks.
        """
        if isinstance(tracks, list):
            if len(tracks) > 50:
                raise ValueError("Maximum tracks to check is 50")

            params = {"ids": ",".join([item.id for item in tracks])}

        else:
            params = {"ids": tracks.id}

        response = self._get(f"{self._library}/tracks/contains", params=params)

        return response.json()[0] if len(response.json()) == 1 else response.json()

    @scope(user_library_read)
    def get_saved_albums(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Generator[SavedAlbum, None, None]:
        """Get a list of the albums saved in the current Spotify user’s ‘Your Music’ library.

        Args:
            limit: The maximum number of objects to return. Default: 20. Minimum: 1. Maximum: 50.
            offset: The index of the first object to return. Default: 0 (i.e., the first object). Use with limit to get
                the next set of objects.

        Raises:
            ValueError:
                If specified `limit` is outside the valid range
                If both `after` and `before` are specified

        Returns:
            A generator of saved albums and their timestamps.
        """
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        params = {"limit": limit, "offset": offset}

        response = self._get(f"{self._library}/albums", params=params)

        return generate(response.json(), SavedAlbum, self._oauth)

    @scope(user_library_read)
    def get_saved_tracks(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Generator[SavedTrack, None, None]:
        """Get a list of the songs saved in the current Spotify user’s ‘Your Music’ library.

        Args:
            limit: The maximum number of objects to return. Default: 20. Minimum: 1. Maximum: 50.
            offset: The index of the first object to return. Default: 0 (i.e., the first object). Use with limit to get
                the next set of objects.

        Raises:
            ValueError:
                If specified `limit` is outside the valid range
                If both `after` and `before` are specified

        Returns:
            A generator of saved tracks and their timestamps.
        """
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        params = {"limit": limit, "offset": offset}

        response = self._get(f"{self._library}/tracks", params=params)

        return generate(response.json(), SavedTrack, self._oauth)

    @scope(user_library_modify)
    def remove_saved_albums(self, albums: Union[Album, List[Album]]):
        """Remove one or more albums from the current user’s ‘Your Music’ library.

        Changes to a user’s saved albums may not be visible in other Spotify applications immediately.

        Args:
            albums: The album or albums to be removed.

        Raises:
            ValueError: If more than 50 albums are provided.
        """
        if isinstance(albums, list):
            if len(albums) > 50:
                raise ValueError("Maximum albums to remove is 50")

            params = {"ids": ",".join([album.id for album in albums])}

        else:
            params = {"ids": albums.id}

        self._delete(f"{self._library}/albums", params=params)

    @scope(user_library_modify)
    def remove_saved_tracks(self, tracks: Union[Track, List[Track]]):
        """Remove one or more tracks from the current user’s ‘Your Music’ library.

        Changes to a user’s saved tracks may not be visible in other Spotify applications immediately.

        Args:
            tracks: The track or tracks to be removed.

        Raises:
            ValueError: If more than 50 tracks are provided.
        """
        if isinstance(tracks, list):
            if len(tracks) > 50:
                raise ValueError("Maximum albums to remove is 50")

            params = {"ids": ",".join([track.id for track in tracks])}

        else:
            params = {"ids": tracks.id}

        self._delete(f"{self._library}/tracks", params=params)

    @scope(user_library_modify)
    def save_albums(self, albums: Union[Album, List[Album]]):
        """Save one or more albums to the current user’s ‘Your Music’ library.

        Args:
            albums: The album or albums to save.

        Raises:
            ValueError: If more than 50 albums are provided.
        """
        if isinstance(albums, list):
            if len(albums) > 50:
                raise ValueError("Maximum albums to save is 50")

            params = {"ids": ",".join([album.id for album in albums])}

        else:
            params = {"ids": albums.id}

        self._put(f"{self._library}/albums", params=params)

    @scope(user_library_modify)
    def save_tracks(self, tracks: Union[Track, List[Track]]):
        """Save one or more tracks to the current user’s ‘Your Music’ library.

        Args:
            tracks: The track or tracks to save.

        Raises:
            ValueError: If more than 50 tracks are provided.
        """
        if isinstance(tracks, list):
            if len(tracks) > 50:
                raise ValueError("Maximum albums to save is 50")

            params = {"ids": ",".join([track.id for track in tracks])}

        else:
            params = {"ids": tracks.id}

        self._put(f"{self._library}/tracks", params=params)
