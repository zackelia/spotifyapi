"""Provide the utils module."""
from typing import Any, Generator
from requests_oauthlib import OAuth2Session

from ..models import Paging


def generate(
    data, object_factory: Any, session: OAuth2Session
) -> Generator[Any, None, None]:
    """Yield all objects for a paging object

    Args:
        data: The initial paging data.
        object_factory: The type of object to yield.
        session: The session used to get the rest of the items in the paging object.

    Returns:
        A generator of the items in the paging object.
    """
    paging = Paging(data, object_factory)

    while True:
        for item in paging.items:
            yield item

        if not paging.next:
            break

        response = session.get(paging.next)
        paging = Paging(response.json(), object_factory)
