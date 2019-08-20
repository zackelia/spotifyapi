"""Provide the endpoint superclass."""
import json
import requests
from typing import Optional
from requests_oauthlib import OAuth2Session

from ..exceptions import ExpiredTokenError, SpotifyAPIError


class EndpointBase:
    """Base endpoint functionality."""

    def __init__(self, oauth: OAuth2Session):
        self._oauth = oauth
        self._base_url = "https://api.spotify.com/v1"

    def __del__(self):
        self._oauth.close()

    def _delete(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(self._oauth.delete, url, **kwargs)

    def _get(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(self._oauth.get, url, **kwargs)

    def _put(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(self._oauth.put, url, **kwargs)

    def _post(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(self._oauth.post, url, **kwargs)

    def __request(
        self, method, url: str, **kwargs
    ) -> Optional[requests.models.Response]:
        # Serialize data to json
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        response = method(url, **kwargs)

        # Check if there's no content so we don't try to create an instance of something
        if response.status_code == requests.codes.no_content:
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if "token expired" in response.json()["error"]["message"]:
                raise ExpiredTokenError(self._oauth.token.access_token)
            raise SpotifyAPIError(response.json()["error"]["message"])

        return response
