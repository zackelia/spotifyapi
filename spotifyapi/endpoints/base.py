"""Provide the endpoint superclass."""
import json
import requests
from typing import Any, Generator, Optional

from ..exceptions import ExpiredTokenError, SpotifyAPIError
from ..models import Paging, Token


class EndpointBase:
    """Base endpoint functionality."""

    def __init__(self, token: Token):
        self._token = token
        self._base_url = "https://api.spotify.com/v1"

    def _get(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.get, url, **kwargs)

    def _put(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.put, url, **kwargs)

    def _post(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.post, url, **kwargs)

    def __request(
        self, method, url: str, **kwargs
    ) -> Optional[requests.models.Response]:
        headers = {"Authorization": "Bearer {}".format(self._token.access_token)}

        # Serialize data to json
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        response = method(url, headers=headers, **kwargs)

        # Check if there's no content so we don't try to create an instance of something
        if response.status_code == requests.codes.no_content:
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if "token expired" in response.json()["error"]["message"]:
                raise ExpiredTokenError(self._token.access_token)
            raise SpotifyAPIError(response.json()["error"]["message"])

        return response

    def _generate(
        self, paging: Paging, object_factory: Any
    ) -> Generator[Any, None, None]:
        # Yield all objects for a paging object
        while True:
            for item in paging.items:
                yield item

            if not paging.next:
                break

            response = self._get(paging.next)
            paging = Paging(response.json(), object_factory)
