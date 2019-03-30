""" This module provides the Track object """
from spotifyapi.artist import Artist


class Track:
    def __init__(self, data):
        # TODO: Add album
        self._artists = [Artist(artist_data) for artist_data in data['artists']]
        self._duration_ms = data['duration_ms']
        self._explicit = data['explicit']
        self._name = data['name']
        self._id = data['id']
        self._popularity = data['popularity']

    @property
    def artists(self):
        """
        The artists who performed the track.
        """
        return self._artists

    @property
    def duration_ms(self):
        """ The track length in milliseconds. """
        return self._duration_ms

    @property
    def explicit(self):
        """ Whether or not the track has explicit lyrics. """
        return self._explicit

    @property
    def id(self):
        """ The Spotify ID for the track. """
        return self._id

    @property
    def name(self):
        """ The name of the track. """
        return self._name

    @property
    def popularity(self):
        """
        The popularity of the track. The value will be between 0 and 100, with 100 being the most popular.

        The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is
        calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how
        recent those plays are.

        Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were
        played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated
        independently. Artist and album popularity is derived mathematically from track popularity. Note that the
        popularity value may lag actual popularity by a few days: the value is not updated in real time.
        """
        return self._popularity
