"""Provide the track endpoint."""
from typing import List, Optional, Union

from .base import EndpointBase
from ..models import AudioAnalysis, AudioFeatures, FullTrack, Token, Track


class TrackEndpoint(EndpointBase):
    """Endpoints for retrieving information about one or more tracks from the Spotify catalog."""

    def __init__(self, token: Token):
        super().__init__(token)

    def get_audio_analysis(self, track: Track) -> AudioAnalysis:
        """Get a detailed audio analysis for a single track.

        The Audio Analysis endpoint provides low-level audio analysis for all of the tracks in the Spotify catalog. The
        Audio Analysis describes the track’s structure and musical content, including rhythm, pitch, and timbre. All
        information is precise to the audio sample.

        Many elements of analysis include confidence values, a floating-point number ranging from 0.0 to 1.0. Confidence
        indicates the reliability of its corresponding attribute. Elements carrying a small confidence value should be
        considered speculative. There may not be sufficient data in the audio to compute the attribute with high
        certainty.

        Args:
            track: The track to get analysis for.

        Returns:
            Audio analysis for the track.
        """
        response = self._get(f"{self._base_url}/audio-analysis/{track.id}")

        return AudioAnalysis(response.json())

    def get_audio_features(
        self, track: Union[Track, List[Track]]
    ) -> Union[AudioFeatures, List[AudioFeatures]]:
        """Get audio feature information for a single or multiple tracks.

        Args:
            track: Either a single track or a list of tracks (max 100).

        Returns:
            Audio features for the track or a list of audio features for the tracks.
        """
        if type(track) is list:
            tracks = track

            if len(tracks) > 100:
                raise ValueError("Maximum track count is 100")

            params = {"ids": ",".join([track.id for track in tracks])}

            response = self._get(f"{self._base_url}/audio-features", params=params)

            return [AudioFeatures(data) for data in response.json()["audio_features"]]

        else:
            response = self._get(f"{self._base_url}/audio-features/{track.id}")

            return AudioFeatures(response.json())

    def get_track(self, id: str) -> FullTrack:
        """Get Spotify catalog information for a single track identified by its unique Spotify ID.

        Args:
            id: The Spotify ID for the track.

        Returns:
            A full track for the ID.
        """
        response = self._get(f"{self._base_url}/tracks/{id}")

        return FullTrack(response.json())

    def get_tracks(self, ids: List[str]) -> List[Optional[FullTrack]]:
        """Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        Args:
            ids: A list of the Spotify IDs for the tracks. Maximum: 50 IDs.

        Returns:
            A list of full tracks for IDs. None for IDs that do not correspond with a track.
        """
        if len(ids) > 50:
            raise ValueError("Maximum track ID count is 50")

        params = {"ids": ",".join(ids)}

        response = self._get(f"{self._base_url}/tracks", params=params)

        return [FullTrack(data) if data else None for data in response.json()["tracks"]]
