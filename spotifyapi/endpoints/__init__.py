from .album import AlbumEndpoint
from .artist import ArtistEndpoint
from .library import LibraryEndpoint
from .player import PlayerEndpoint
from .track import TrackEndpoint
from .user import UserEndpoint
from ..models.token import Token



class SpotifyEndpoint(
    AlbumEndpoint, ArtistEndpoint, LibraryEndpoint, PlayerEndpoint, TrackEndpoint, UserEndpoint
):
    """Endpoint class that has functionality of all endpoints."""

    def __init__(self, token: Token):
        super().__init__(token)
