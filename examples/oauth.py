import os
import json
from pathlib import Path
from requests_oauthlib import OAuth2Session

from spotifyapi.endpoints import SpotifyEndpoint
from spotifyapi.authorization import AUTHORIZE_URL, TOKEN_URL
from spotifyapi.authorization.scopes import user_read_currently_playing

# You will either need to set these environment variables or hard-code them here.
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SCOPE = [user_read_currently_playing]


def save_token(token):
    """Saves token to our cache."""
    token_path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath(
        Path(".cache/token")
    )
    with open(token_path, "w") as file:
        file.write(json.dumps(token))


def load_token():
    """Loads a token from our cache. Returns None if no token exists."""
    token_path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath(
        Path(".cache/token")
    )
    try:
        with open(token_path, "r") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


token = load_token()

# Check if we have a token in the cache already.
if not token:
    # First, you will need to get an authorization token for the user. This code will only have to be run once. Once you
    # obtain a token, be sure to save it somewhere so it can be used again without going through the authorization
    # process.
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)

    authorization_url, _ = oauth.authorization_url(AUTHORIZE_URL)

    print(f"Please go to {authorization_url} and authorize access.")
    authorization_response = input("Enter the full callback URL: ")

    token = oauth.fetch_token(
        TOKEN_URL,
        authorization_response=authorization_response,
        client_secret=CLIENT_SECRET,
    )

    # Save this token in a cache somewhere so it can be loaded at a later time.
    save_token(token)

# Optionally, create an instance of OAuth that will auto refresh the token and pass that to spotifyapi.
EXTRA = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}

oauth = OAuth2Session(
    CLIENT_ID,
    token=token,
    auto_refresh_url=TOKEN_URL,
    auto_refresh_kwargs=EXTRA,
    token_updater=save_token,
)

# Test that the token works on an endpoint
spotify = SpotifyEndpoint(oauth)

me = spotify.get_current_user()

print(me.display_name)
