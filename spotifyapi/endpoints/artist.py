"""Provide the artist endpoint."""
from typing import Generator, List, Optional
from .base import EndpointBase
from ..models import FullArtist, FullTrack, Paging, SimplifiedAlbum, Token


class ArtistEndpoint(EndpointBase):
    """Endpoints for retrieving information about one or more artists from the Spotify catalog."""

    def __init__(self, token: Token):
        super().__init__(token)

        self._artists = f"{self._base_url}/artists"

    def get_artist(self, id: str) -> FullArtist:
        """Get Spotify catalog information for a single artist.

        Args:
            id: The Spotify Id for the artist.

        Returns:
            The artist with the specified ID.
        """
        response = self._get(f"{self._artists}/{id}")

        return FullArtist(response.json())

    def get_artist_albums(
        self,
        id: str,
        include_groups: Optional[List[str]] = None,
        country: Optional[str] = "US",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Generator[SimplifiedAlbum, None, None]:
        """Get Spotify catalog information about an artist’s albums.

        Args:
            id: The Spotify Id for the artist.
            include_groups: A comma-separated list of keywords that will be used to filter the response.
                If not supplied, all album types will be returned. Valid values are:
                    - album
                    - single
                    - appears_on
                    - compilation
                For example: include_groups=album,single.
            country: An ISO 3166-1 alpha-2 country code or the string from_token.
                Supply this parameter to limit the response to one particular geographical market. For example, for
                albums available in Sweden: country=SE. If not given, results will be returned for all countries and you
                are likely to get duplicate results per album, one for each country in which the album is available!
            limit: The number of album objects to return. Default: 20. Minimum: 1. Maximum: 50. For example: limit=2
            offset: The index of the first album to return. Default: 0 (i.e., the first album). Use with limit to get
                the next set of albums.
        Returns:
            A generator of the artist's albums.
        """
        # If limit is specified, check that it is a legitimate value
        if limit and not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        if offset and not limit:
            raise ValueError("limit must be used with offset")

        params = {"country": country, "limit": limit, "offset": offset}

        if include_groups:
            params["include_groups"] = ",".join(include_groups)

        response = self._get(f"{self._artists}/{id}/albums", params=params)

        paging = Paging(response.json(), SimplifiedAlbum)

        return self._generate(paging, SimplifiedAlbum)

    def get_artist_top_tracks(self, id: str, country: str = "US") -> List[FullTrack]:
        """Get Spotify catalog information about an artist’s top tracks by country.

        Args:
            id: The Spotify Id for the artist.
            country: An ISO 3166-1 alpha-2 country code or the string from_token.

        Returns:
            The artist's top tracks by country.
        """
        params = {"country": country}

        if not country:
            raise ValueError("Country must be defined")

        response = self._get(f"{self._artists}/{id}/top-tracks", params=params)

        return [FullTrack(track) for track in response.json()["tracks"]]

    def get_related_artists(self, id: str) -> List[FullArtist]:
        """Get Spotify catalog information about artists similar to a given artist. Similarity is based on analysis of
        the Spotify community’s listening history.

        Args:
            id: The Spotify Id for the artist.

        Returns:
            Artists similar to the given artist.
        """
        response = self._get(f"{self._artists}/{id}/related-artists")

        return [FullArtist(artist) for artist in response.json()["artists"]]

    def get_artists(self, ids: List[str]) -> List[FullArtist]:
        """Get Spotify catalog information for several artists

        Args:
            ids: The Spotify Id for the artist.

        Returns:
            Information on several artists.
        """
        if len(ids) > 50:
            raise ValueError("Maximum artist ID count is 50")

        params = {"ids": ",".join(ids)}

        response = self._get(f"{self._artists}", params=params)

        return [FullArtist(artist) for artist in response.json()["artists"]]
