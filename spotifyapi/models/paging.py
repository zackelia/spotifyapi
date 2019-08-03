"""Provide the paging model."""
from typing import Any, Dict, List, Optional


class Paging:
    """
    The offset-based paging object is a container for a set of objects. It contains a key called items (whose value is
    an array of the requested objects) along with other keys like previous, next and limit that can be useful in future
    calls.
    """

    def __init__(self, data, object_factory: Any):
        self._href = data["href"]
        self._items = [object_factory(d) for d in data["items"]]
        self._limit = data["limit"]
        self._next = data["next"]

        self._obj = object_factory

    @property
    def href(self) -> str:
        """A link to the Web API endpoint returning the full result of the request."""
        return self._href

    @property
    def items(self) -> List[Any]:
        """The requested data."""
        return self._items

    @property
    def limit(self) -> int:
        """The maximum number of items in the response (as set in the query or by default)."""
        return self._limit

    @property
    def next(self) -> Optional[str]:
        """URL to the next page of items."""
        return self._next
