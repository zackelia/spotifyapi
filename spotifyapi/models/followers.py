"""Provide the followers model."""
from typing import Optional


class Followers:
    """The total followers."""

    def __init__(self, data):
        self._href = data["href"]
        self._total = data["total"]

    @property
    def href(self) -> Optional[str]:
        """
        A link to the Web API endpoint providing full details of the followers Please note that this will always be set
        to null, as the Web API does not support it at the moment.
        """
        return self._href

    @property
    def total(self) -> int:
        """The total number of followers."""
        return self._total
