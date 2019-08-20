"""Provide the utils module."""
from typing import Any, Generator
from requests import Session

from ..models import Paging


def generate(paging: Paging, session: Session) -> Generator[Any, None, None]:
    """Yield all objects for a paging object

    Args:
        paging: The paging object to yield from.
        session: The session used to get the rest of the items in the paging object.

    Returns:
        A generator of the items in the paging object.
    """
    object_factory = paging.object_factory

    while True:
        for item in paging.items:
            yield item

        if not paging.next:
            break

        response = session.get(paging.next)
        paging = Paging(response.json(), object_factory)
