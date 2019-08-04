# spotifyapi

spotifyapi is a Python wrapper to interact with the Spotify web API. spotifyapi attempts to stay as close as possible to
the original API calls while implementing more Pythonic features.

## Installation

spotifyapi supports Python 3.6 and higher and can be installed through Pip.

```pip install spotifyapi```

## Example

The easiest way to use spotifyapi is using the SpotifyEndpoint which implements all methods of the package. However, it
is still possible to use the individual endpoints such as AlbumEndpoint, PlayerEndpoint, etc.

```python
from spotifyapi import SpotifyEndpoint

spotify = SpotifyEndpoint(token)

# Print out all of the recently played songs
for recent in spotify.get_recently_played_tracks():
    print(recent.track.name)

# Change playback on the device
spotify.next()
spotify.volume(100)
```