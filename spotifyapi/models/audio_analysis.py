"""Provide the audio analysis model."""
from typing import List

from .section import Section
from .segment import Segment
from .time_interval import TimeInterval


class AudioAnalysis:
    """
    The track’s structure and musical content, including rhythm, pitch, and timbre. All information is precise to the
    audio sample.
    """

    def __init__(self, data):
        self._bars = [TimeInterval(d) for d in data["bars"]]
        self._beats = [TimeInterval(d) for d in data["beats"]]
        self._sections = [Section(d) for d in data["sections"]]
        self._segments = [Segment(d) for d in data["segments"]]
        self._tatums = [TimeInterval(d) for d in data["tatums"]]

    @property
    def bars(self) -> List[TimeInterval]:
        """
        The time intervals of the bars throughout the track. A bar (or measure) is a segment of time defined as a given
        number of beats. Bar offsets also indicate downbeats, the first beat of the measure.
        """
        return self._bars

    @property
    def beats(self) -> List[TimeInterval]:
        """
        The time intervals of beats throughout the track. A beat is the basic time unit of a piece of music; for
        example, each tick of a metronome. Beats are typically multiples of tatums.
        """
        return self._beats

    @property
    def sections(self) -> List[Section]:
        """
        Sections are defined by large variations in rhythm or timbre, e.g. chorus, verse, bridge, guitar solo, etc. Each
        section contains its own descriptions of tempo, key, mode, time_signature, and loudness.
        """
        return self._sections

    @property
    def segments(self) -> List[Segment]:
        """
        Audio segments attempts to subdivide a song into many segments, with each segment containing a roughly
        consistent sound throughout its duration.
        """
        return self._segments

    @property
    def tatums(self) -> List[TimeInterval]:
        """
        A tatum represents the lowest regular pulse train that a listener intuitively infers from the timing of
        perceived musical events (segments). For more information about tatums, see
        https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/#rhythm
        """
        return self._tatums
