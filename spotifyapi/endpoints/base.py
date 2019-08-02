"""Provide the endpoint superclass."""
import json
import requests

from ..exceptions import ExpiredTokenError, SpotifyAPIError


class EndpointBase:
    """Base endpoint functionality."""

    def __init__(self, access_token: str):
        self._access_token = access_token
        self._url = "https://api.spotify.com/v1"

    def _get(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.get, url, **kwargs)

    def _put(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.put, url, **kwargs)

    def _post(self, url: str, **kwargs) -> requests.models.Response:
        return self.__request(requests.post, url, **kwargs)

    def __request(self, method, url: str, **kwargs) -> requests.models.Response:
        headers = {"Authorization": "Bearer {}".format(self._access_token)}

        # Serialize data to json
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        response = method(url, headers=headers, **kwargs)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if "token expired" in response.json()["error"]["message"]:
                raise ExpiredTokenError(self._access_token)
            raise SpotifyAPIError(response.json()["error"]["message"])

        return response
