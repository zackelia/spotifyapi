from .album import AlbumEndpoint
from .player import PlayerEndpoint


class SpotifyEndpoint(AlbumEndpoint, PlayerEndpoint):
    """Endpoint class that has functionality of all endpoints."""

    def __init__(self, access_token: str):
        super().__init__(access_token)
