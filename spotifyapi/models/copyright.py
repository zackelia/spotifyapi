"""Provide the copyright model."""


class Copyright:
    """The copyright information of an album."""

    def __init__(self, data):
        self._text = data["text"]
        self._type = data["type"]

    @property
    def text(self) -> str:
        """The copyright text for this album."""
        return self._text

    @property
    def type(self) -> str:
        """The type of copyright: C = the copyright, P = the sound recording (performance) copyright."""
        return self._type
