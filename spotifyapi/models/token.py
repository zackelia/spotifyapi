"""Provide the token module."""
import base64
import datetime
import json

import requests


class Token:
    """The token response from Spotify authorization."""

    def __init__(self, data):
        self._access_token = data["access_token"]
        self._token_type = data["token_type"]
        self._scope = data["scope"]
        self._expires_in = data["expires_in"]
        self._refresh_token = data["refresh_token"]
        self._creation = (
            datetime.datetime.strptime(data["creation"], "%Y-%m-%d %H:%M:%S.%f")
            if "creation" in data
            else datetime.datetime.now()
        )

    def __str__(self):
        return json.dumps(
            {
                "access_token": self._access_token,
                "token_type": self._token_type,
                "scope": self._scope,
                "expires_in": self._expires_in,
                "refresh_token": self._refresh_token,
                "creation": str(self._creation),
            }
        )

    @property
    def access_token(self) -> str:
        """The token used to make requests."""
        return self._access_token

    @property
    def token_type(self) -> str:
        """Type of token."""
        return self._token_type

    @property
    def scope(self) -> str:
        """Scopes of the token."""
        return self._scope

    @property
    def expires_in(self) -> int:
        """How long the token is valid before refreshing."""
        return self._expires_in

    @property
    def refresh_token(self) -> str:
        """The token used to refresh the authorization token."""
        return self._refresh_token

    @property
    def creation(self) -> datetime.datetime:
        """The time the token was created."""
        return self._creation

    def is_expired(self) -> bool:
        """Returns True if the token is expired, False otherwise."""
        return (
            self._creation + datetime.timedelta(seconds=self._expires_in)
            < datetime.datetime.now()
        )

    def refresh(self, client_id: str, client_secret: str) -> None:
        """Refreshes the token if needed."""
        url = "https://accounts.spotify.com/api/token"

        # No need to refresh if the token isn't expired.
        if not self.is_expired():
            return

        data = {"grant_type": "refresh_token", "refresh_token": self._refresh_token}

        authorization = base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()

        headers = {"Authorization": f"Basic {authorization}"}

        response = requests.post(url, data=data, headers=headers)

        self._access_token = response.json()["access_token"]
        self._token_type = response.json()["token_type"]
        self._scope = response.json()["scope"]
        self._expires_in = response.json()["expires_in"]
        self._creation = datetime.datetime.now()
