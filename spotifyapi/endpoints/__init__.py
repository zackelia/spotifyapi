from .album import AlbumEndpoint
from .artist import ArtistEndpoint
from .player import PlayerEndpoint
from ..models.token import Token


class SpotifyEndpoint(AlbumEndpoint, ArtistEndpoint, PlayerEndpoint):
    """Endpoint class that has functionality of all endpoints."""

    def __init__(self, token: Token):
        super().__init__(token)
