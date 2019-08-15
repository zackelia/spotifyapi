"""Provide the section model."""


class Section:
    """A section of a track that is relatively uniform."""

    def __init__(self, data):
        self._start = data["start"]
        self._duration = data["duration"]
        self._confidence = data["confidence"]
        self._loudness = data["loudness"]
        self._tempo = data["tempo"]
        self._tempo_confidence = data["tempo_confidence"]
        self._key = data["key"]
        self._key_confidence = data["key_confidence"]
        self._mode = data["mode"]
        self._mode_confidence = data["mode_confidence"]
        self._time_signature = data["time_signature"]
        self._time_signature_confidence = data["time_signature_confidence"]

    @property
    def start(self) -> float:
        """The starting point (in seconds) of the section."""
        return self._start

    @property
    def duration(self) -> float:
        """The duration (in seconds) of the section."""
        return self._duration

    @property
    def confidence(self) -> float:
        """The confidence, from 0.0 to 1.0, of the reliability of the section’s “designation”."""
        return self._confidence

    @property
    def loudness(self) -> float:
        """
        The overall loudness of the section in decibels (dB). Loudness values are useful for comparing relative loudness
        of sections within tracks.
        """
        return self._loudness

    @property
    def tempo(self) -> float:
        """
        The overall estimated tempo of the section in beats per minute (BPM). In musical terminology, tempo is the speed
        or pace of a given piece and derives directly from the average beat duration.
        """
        return self._tempo

    @property
    def tempo_confidence(self) -> float:
        """
        The confidence, from 0.0 to 1.0, of the reliability of the tempo. Some tracks contain tempo changes or sounds
        which don’t contain tempo (like pure speech) which would correspond to a low value in this field.
        """
        return self._tempo_confidence

    @property
    def key(self) -> int:
        """
        The estimated overall key of the section. The values in this field ranging from 0 to 11 mapping to pitches using
        standard Pitch Class notation (E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on). If no key was detected, the value is
        -1.
        """
        return self._key

    @property
    def key_confidence(self) -> float:
        """
        The confidence, from 0.0 to 1.0, of the reliability of the key. Songs with many key changes may correspond to
        low values in this field.
        """
        return self._key_confidence

    @property
    def mode(self) -> int:
        """
        Indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.
        This field will contain a 0 for “minor”, a 1 for “major”, or a -1 for no result. Note that the major key (e.g.
        C major) could more likely be confused with the minor key at 3 semitones lower (e.g. A minor) as both keys carry
        the same pitches.
        """
        return self._mode

    @property
    def mode_confidence(self) -> float:
        """The confidence, from 0.0 to 1.0, of the reliability of the mode."""
        return self._mode_confidence

    @property
    def time_signature(self) -> int:
        """
        An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify
        how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of
        “3/4”, to “7/4”.
        """
        return self._time_signature

    @property
    def time_signature_confidence(self) -> float:
        """
        The confidence, from 0.0 to 1.0, of the reliability of the time_signature. Sections with time signature changes
        may correspond to low values in this field.
        """
        return self._time_signature_confidence
