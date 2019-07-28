"""Provide the context model."""
from typing import Dict, Optional


class Context:
    """An item's context."""

    def __init__(self, data):
        self._uri = data["uri"]
        self._href = data["href"]
        self._external_urls = data["external_urls"]
        self._type = data["type"]

    @property
    def uri(self) -> str:
        """The uri of the context."""
        return self._uri

    @property
    def href(self) -> Optional[str]:
        """The href of the context, or None if not available."""
        return self._href

    @property
    def external_urls(self) -> Optional[Dict[str, str]]:
        """The external_urls of the context, or None if not available."""
        return self._external_urls

    @property
    def type(self) -> str:
        """The object type of the item’s context. Can be one of album , artist or playlist."""
        return self._type
