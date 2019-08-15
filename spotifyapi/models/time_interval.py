"""Provide the time interval model."""


class TimeInterval:
    """A generic object used to represent various time intervals within Audio Analysis."""

    def __init__(self, data):
        self._start = data["start"]
        self._duration = data["duration"]
        self._confidence = data["confidence"]

    @property
    def start(self) -> float:
        """The starting point (in seconds) of the time interval."""
        return self._start

    @property
    def duration(self) -> float:
        """The duration (in seconds) of the time interval."""
        return self._duration

    @property
    def confidence(self) -> float:
        """The confidence, from 0.0 to 1.0, of the reliability of the interval."""
        return self._confidence
