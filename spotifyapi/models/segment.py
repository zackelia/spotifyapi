"""Provide the segment model."""
from typing import List


class Segment:
    """A segment of a track that is relatively uniform."""

    def __init__(self, data):
        self._start = data["start"]
        self._duration = data["duration"]
        self._confidence = data["confidence"]
        self._loudness_start = data["loudness_start"]
        self._loudness_max = data["loudness_max"]
        self._loudness_max_time = data["loudness_max_time"]
        self._pitches = data["pitches"]
        self._timbre = data["timbre"]

    @property
    def start(self) -> float:
        """The starting point (in seconds) of the segment."""
        return self._start

    @property
    def duration(self) -> float:
        """The duration (in seconds) of the segment."""
        return self._duration

    @property
    def confidence(self) -> float:
        """
        The confidence, from 0.0 to 1.0, of the reliability of the segmentation. Segments of the song which are
        difficult to logically segment (e.g: noise) may correspond to low values in this field.
        """
        return self._confidence

    @property
    def loudness_start(self) -> float:
        """
        The onset loudness of the segment in decibels (dB). Combined with loudness_max and loudness_max_time, these
        components can be used to describe the “attack” of the segment.
        """
        return self._loudness_start

    @property
    def loudness_max(self) -> float:
        """
        The peak loudness of the segment in decibels (dB). Combined with loudness_start and loudness_max_time, these
        components can be used to describe the “attack” of the segment.
        """
        return self._loudness_max

    @property
    def loudness_max_time(self) -> float:
        """
        The segment-relative offset of the segment peak loudness in seconds. Combined with loudness_start and
        loudness_max, these components can be used to describe the “attack” of the segment.
        """
        return self._loudness_max_time

    @property
    def pitches(self) -> List[float]:
        """
        A “chroma” vector representing the pitch content of the segment, corresponding to the 12 pitch classes C, C#, D
        to B, with values ranging from 0 to 1 that describe the relative dominance of every pitch in the chromatic
        scale. More details about how to interpret this vector can be found at
        https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/#pitch
        """
        return self._pitches

    @property
    def timbre(self) -> List[float]:
        """
        Timbre is the quality of a musical note or sound that distinguishes different types of musical instruments, or
        voices. Timbre vectors are best used in comparison with each other. More details about how to interpret this
        vector can be found at
        https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/#timbre.
        """
        return self._timbre
