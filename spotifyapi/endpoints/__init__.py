from requests_oauthlib import OAuth2Session

from .album import AlbumEndpoint
from .artist import ArtistEndpoint
from .library import LibraryEndpoint
from .player import PlayerEndpoint
from .playlist import PlaylistEndpoint
from .track import TrackEndpoint
from .user import UserEndpoint


class SpotifyEndpoint(
    AlbumEndpoint,
    ArtistEndpoint,
    LibraryEndpoint,
    PlayerEndpoint,
    PlaylistEndpoint,
    TrackEndpoint,
    UserEndpoint,
):
    """Endpoint class that has functionality of all endpoints."""

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)
