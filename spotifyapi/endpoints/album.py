"""Provide the album endpoint."""
from typing import Generator, List, Optional
from requests_oauthlib import OAuth2Session

from .base import EndpointBase
from ..models import Album, FullAlbum, SimplifiedTrack, Paging
from ..utils import generate


class AlbumEndpoint(EndpointBase):
    """Endpoints for retrieving information about one or more albums from the Spotify catalog."""

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)

        self._albums = f"{self._base_url}/albums"

    def get_album(self, id: str) -> FullAlbum:
        """Get Spotify catalog information for a single album.

        Args:
            id: The Spotify ID for the album.

        Returns:
            The album with specified ID.
        """
        response = self._get(f"{self._albums}/{id}")

        return FullAlbum(response.json())

    def get_album_tracks(
        self, album: Album, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Generator[SimplifiedTrack, None, None]:
        """Get Spotify catalog information about an album’s tracks. Optional parameters can be used to limit the number
            of tracks returned.

        Args:
            album: The Album object.
            limit: The maximum number of tracks to return. Minimum: 1. Maximum: 50.
            offset: The index of the first track to return. Use with limit to get the next set of tracks.

        Returns:
            A generator of simplified tracks.
        """
        # If limit is specified, check that it is a legitimate value
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        params = {"limit": limit, "offset": offset}

        response = self._get(f"{self._albums}/{album.id}/tracks", params=params)

        paging = Paging(response.json(), SimplifiedTrack)

        return generate(paging, self._oauth)

    def get_albums(self, ids: List[str]) -> List[Optional[FullAlbum]]:
        """Get Spotify catalog information for multiple albums identified by their Spotify IDs.

        Args:
            ids: A list of the Spotify IDs for the albums. Maximum: 20 IDs.

        Returns:
            List of albums for IDs. IDs not corresponding to an album give None.
        """
        if len(ids) > 20:
            raise ValueError("Maximum album ID count is 20")

        params = {"ids": ",".join(ids)}

        response = self._get(f"{self._albums}", params=params)

        return [FullAlbum(data) if data else None for data in response.json()["albums"]]
