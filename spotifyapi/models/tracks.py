"""Provide the tracks model."""


class Tracks:
    """A description of the tracks from a simplified playlist object."""

    def __init__(self, data):
        self._href = data["href"]
        self._total = data["total"]

    @property
    def href(self):
        """Link to the full tracks."""
        return self._href

    @property
    def total(self):
        """Total number of tracks."""
        return self._total
