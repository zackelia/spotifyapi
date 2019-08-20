# spotifyapi

[![PyPI](https://img.shields.io/pypi/v/spotifyapi.svg)](https://pypi.python.org/pypi/spotifyapi/)
[![PyPI](https://img.shields.io/pypi/pyversions/spotifyapi.svg)](https://pypi.python.org/pypi/spotifyapi/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

spotify = SpotifyEndpoint(oauth)

# Get the currently playing track
playing = spotify.get_currently_playing().item

# Get the track's features using Spotify's machine learning
features = spotify.get_audio_features(playing)

# Time to party!
if features.danceability > 0.75:
    spotify.volume(100)
```

## Contributing

*spotifyapi* is open to contributions! Either take a look at the list of issues or submit your own. In order to develop on *spotifyapi*, follow this guide:

1. Fork and clone the repository locally
2. Setup a virtual environment
    - `python3.6 -m venv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements-dev.txt`
    - `pre-commit install`
3. Develop following the [Spotify API guide](https://developer.spotify.com/documentation/web-api/reference/)
4. Commit changes and submit a pull request
