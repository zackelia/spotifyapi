import os
from pathlib import Path
import webbrowser

from spotifyapi.endpoints import SpotifyEndpoint
from spotifyapi.utils.oauth import OAuth
from spotifyapi.utils.scope import user_read_currently_playing

# Setup client variables
REDIRECT_URI = "XXXX"
CLIENT_ID = "XXXX"
CLIENT_SECRET = "XXXX"
SCOPE = [user_read_currently_playing]

# Setup OAuth
oauth = OAuth()
token_path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath(Path(".cache/token"))

# Attempt to load a token from the cache
try:
    with open(token_path, "r") as file:
        token = oauth.parse_token(file.read())
except FileNotFoundError:
    token = None

# Go through authorization to get a token, if necessary
if not token:
    url = oauth.get_authorization_url(CLIENT_ID, REDIRECT_URI, scope=SCOPE)
    webbrowser.open(url)

    authorization_url = input("Enter the url you were redirected to: ").strip()
    code, _ = oauth.callback(authorization_url)

    token = oauth.request_access_token(code, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET)

    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, "w") as file:
        file.write(str(token))

# Check if the current token is expired and refresh if applicable
if token.is_expired():
    token.refresh(CLIENT_ID, CLIENT_SECRET)

    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, "w") as file:
        file.write(str(token))

# Test that the token works on an endpoint
spotify = SpotifyEndpoint(token)

track = spotify.get_currently_playing_track()
print(track.item.name)
