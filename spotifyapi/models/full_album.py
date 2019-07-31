"""Provide the full album model."""
from typing import Dict, List

from .copyright import Copyright
from .paging import Paging
from .simplified_album import SimplifiedAlbum
from .simplified_track import SimplifiedTrack


class FullAlbum(SimplifiedAlbum):
    """A full album."""

    def __init__(self, data):
        super().__init__(data)

        self._copyrights = [Copyright(d) for d in data["copyrights"]]
        self._external_ids = data["external_ids"]
        self._genres = data["genres"]
        self._label = data["label"]
        self._popularity = data["popularity"]
        self._tracks = Paging(data["tracks"], SimplifiedTrack)

    @property
    def copyrights(self) -> List[Copyright]:
        """The copyright statements of the album."""
        return self._copyrights

    @property
    def external_ids(self) -> Dict[str, str]:
        """Known external IDs for the album."""
        return self._external_ids

    @property
    def genres(self) -> List[str]:
        """A list of the genres used to classify the album. For example: "Prog Rock" , "Post-Grunge"."""
        return self._genres

    @property
    def label(self) -> str:
        """The label for the album."""
        return self._label

    @property
    def popularity(self) -> int:
        """
        The popularity of the album. The value will be between 0 and 100, with 100 being the most popular. The
        popularity is calculated from the popularity of the album’s individual tracks.
        """
        return self._popularity

    @property
    def tracks(self) -> Paging:
        """The tracks of the album."""
        return self._tracks
