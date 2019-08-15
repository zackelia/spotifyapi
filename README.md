# spotifyapi

*spotifyapi* is a modern Python wrapper to interact with the Spotify web API. *spotifyapi* attempts to stay as close as possible to
the original API calls while implementing more Pythonic features.

## Installation

*spotifyapi* supports Python 3.6 and higher and can be installed through Pip.

```pip install spotifyapi```

## Example

The easiest way to use *spotifyapi* is using the SpotifyEndpoint which implements all methods of the package. However, it
is still possible to use the individual endpoints such as AlbumEndpoint, PlayerEndpoint, etc.

```python
from spotifyapi import SpotifyEndpoint

spotify = SpotifyEndpoint(token)

# Get the currently playing track
playing = spotify.get_currently_playing_track().item

# Get the track's features using Spotify's machine learning
features = spotify.get_audio_features(playing)

# Time to party!
if features.danceability > 0.75:
    spotify.volume(100)
```
