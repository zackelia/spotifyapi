""" This module provides the artist object """


class Artist:
    def __init__(self, data):
        self._id = data['id']
        self._name = data['name']

    @property
    def id(self):
        """ The Spotify ID for the artist. """
        return self._id

    @property
    def name(self):
        """ The name of the artist """
        return self._name
