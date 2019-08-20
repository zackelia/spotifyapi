from requests_oauthlib import OAuth2Session

from .album import AlbumEndpoint
from .artist import ArtistEndpoint
from .library import LibraryEndpoint
from .player import PlayerEndpoint
from .track import TrackEndpoint
from .user import UserEndpoint


class SpotifyEndpoint(
    AlbumEndpoint,
    ArtistEndpoint,
    LibraryEndpoint,
    PlayerEndpoint,
    TrackEndpoint,
    UserEndpoint,
):
    """Endpoint class that has functionality of all endpoints."""

    def __init__(self, oauth: OAuth2Session):
        super().__init__(oauth)
