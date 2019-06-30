"""Provide the paging model."""
from typing import Any, List, Optional


class Paging:
    """
    The offset-based paging object is a container for a set of objects. It contains a key called items (whose value is
    an array of the requested objects) along with other keys like previous, next and limit that can be useful in future
    calls.
    """

    def __init__(self, data, obj: Any):
        self._href = data["href"]
        self._items = [obj(d) for d in data["items"]]
        self._limit = data["limit"]
        self._next = data["next"]
        self._offset = data["offset"]
        self._previous = data["previous"]
        self._total = data["total"]

        self._obj = obj

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

    @property
    def offset(self) -> int:
        """The offset of the items returned (as set in the query or by default)."""
        return self._offset

    @property
    def previous(self) -> Optional[str]:
        """URL to the previous page of items."""
        return self._previous

    @property
    def total(self) -> int:
        """The maximum number of items available to return."""
        return self._total
