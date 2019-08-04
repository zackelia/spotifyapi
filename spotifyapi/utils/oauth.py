"""Provide the oauth module."""
import base64
import json
from typing import List, Optional, Tuple
from urllib.parse import urlparse, parse_qs

import requests

from ..models.token import Token


class OAuth:
    """Provides the methods to support Spotify authorization OAuth."""

    def __init__(self):
        pass

    @staticmethod
    def get_authorization_url(
        client_id: str,
        redirect_uri: str,
        state: Optional[str] = None,
        scope: Optional[List[str]] = None,
        show_dialog: Optional[bool] = False,
    ) -> str:
        """Get the authorization url to request a token with.

        Args:
            client_id: When you register your application, Spotify provides you a Client ID.
            redirect_uri: The URI to redirect to after the user grants or denies permission. This URI needs to have been
                entered in the Redirect URI whitelist that you specified when you registered your application. The value
                of redirect_uri here must exactly match one of the values you entered when you registered your
                application, including upper or lowercase, terminating slashes, and such.
            state: The state can be useful for correlating requests and responses. Because your redirect_uri can be
                guessed, using a state value can increase your assurance that an incoming connection is the result of an
                authentication request. If you generate a random string, or encode the hash of some client state, such
                as a cookie, in this state variable, you can validate the response to additionally ensure that both the
                request and response originated in the same browser. This provides protection against attacks such as
                cross-site request forgery. See RFC-6749.
            scope: A space-separated list of scopes.If no scopes are specified, authorization will be granted only to
                access publicly available information: that is, only information normally visible in the Spotify
                desktop, web, and mobile players.
            show_dialog: Whether or not to force the user to approve the app again if they’ve already done so. If false
                (default), a user who has already approved the application may be automatically redirected to the URI
                specified by redirect_uri. If true, the user will not be automatically redirected and will have to
                approve the app again.

        Returns:
            The authorization URL to request.
        """
        url = "https://accounts.spotify.com/authorize"

        if not scope:
            scope = []

        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": ",".join(scope),
            "show_dialog": show_dialog,
        }

        return requests.Request("GET", url, params=params).prepare().url

    @staticmethod
    def callback(url: str) -> Tuple[str, str]:
        """Parse the callback url for parameters.

        Args:
            url: The callback url the user was sent to after authorizing.

        Raises:
            ValueError: If the user did not accept or if an invalid url is provided.

        Returns:
            A tuple of the authorization code and (if provided) the state.

        """
        query = parse_qs(urlparse(url).query)

        if "code" in query:
            if "state" in query:
                return query["code"][0], query["state"][0]
            return query["code"][0], ""

        elif "error" in query:
            raise ValueError(f"{query['error'][0]}")

        else:
            raise ValueError("Invalid callback url")

    @staticmethod
    def request_access_token(
        code: str, redirect_uri: str, client_id: str, client_secret: str
    ) -> Token:
        url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        authorization = base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()

        headers = {"Authorization": f"Basic {authorization}"}

        response = requests.post(url, data=data, headers=headers)

        return Token(response.json())

    @staticmethod
    def parse_token(contents: str) -> Token:
        """Converts str(token) back to a token object.

        Args:
            contents: The stringified version of a token.

        Returns:
            A corresponding token.
        """
        return Token(json.loads(contents))
