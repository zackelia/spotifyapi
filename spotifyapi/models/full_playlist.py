"""Provide the full playlist model."""
from typing import Generator, Optional

from .followers import Followers
from .paging import Paging
from .playlist import Playlist
from .playlist_track import PlaylistTrack


class FullPlaylist(Playlist):
    """A full playlist."""

    def __init__(self, data, oauth):
        super().__init__(data)
        self._oauth = oauth  # Used to generate tracks

        self._description = data["description"]
        self._followers = Followers(data["followers"])
        self._tracks = data["tracks"]

    @property
    def description(self) -> Optional[str]:
        """The playlist description. Only returned for modified, verified playlists, otherwise None."""
        return self._description

    @property
    def followers(self):
        """Information about the followers of the playlist."""
        return self._followers

    @property
    def tracks(self) -> Generator[PlaylistTrack, None, None]:
        """Information about the tracks of the playlist."""
        paging = Paging(self._tracks, PlaylistTrack)

        while True:
            for item in paging.items:
                yield item

            if not paging.next:
                break

            response = self._oauth.get(paging.next)
            paging = Paging(response.json(), PlaylistTrack)
