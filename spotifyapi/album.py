""" This module provides the album object """


class Album:
    def __init__(self, data):
        self._id = data['id']
        self._images = data['images']
        self._name = data['name']
        self._release_date = data['release_date']

    @property
    def id(self):
        """ The Spotify ID for the album. """
        return self._id

    @property
    def images(self):
        """ The cover art for the album in various sizes, widest first. """
        return self._images

    @property
    def name(self):
        """ The name of the album. In case of an album takedown, the value may be an empty string. """
        return self._name

    @property
    def release_date(self):
        """
        The date the album was first released, for example 1981. Depending on the precision, it might be shown as
        1981-12 or 1981-12-15.
        """
        return self._release_date
