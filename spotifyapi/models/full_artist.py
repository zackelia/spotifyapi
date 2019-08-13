"""Provide the full artist model."""
from typing import List

from .followers import Followers
from .image import Image
from .simplified_artist import SimplifiedArtist


class FullArtist(SimplifiedArtist):
    """A full artist."""

    def __init__(self, data):
        super().__init__(data)

        self._followers = data["followers"]
        self._genres = data["genres"]
        self._images = data["images"]
        self._popularity = data["popularity"]

    @property
    def followers(self) -> Followers:
        """Information about the followers of the artist."""
        return self._followers

    @property
    def genres(self) -> List[str]:
        """
        A list of the genres the artist is associated with. For example: "Prog Rock" , "Post-Grunge". (If not yet
        classified, the array is empty.)
        """
        return self._genres

    @property
    def images(self) -> List[Image]:
        """Images of the artist in various sizes, widest first."""
        return self._images

    @property
    def popularity(self) -> int:
        """
        The popularity of the artist. The value will be between 0 and 100, with 100 being the most popular. The artist’s
        popularity is calculated from the popularity of all the artist’s tracks.
        """
        return self._popularity
