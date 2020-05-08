"""Provide the private user model."""
from typing import Optional
from .user import User


class PrivateUser(User):
    """Private user profile."""

    def __init__(self, data):
        super().__init__(data)

        self._country = data["country"] if "country" in data else None
        self._email = data["email"] if "email" in data else None
        self._product = data["product"] if "product" in data else None

    @property
    def country(self) -> Optional[str]:
        """The country of the user, as set in the user’s account profile. An ISO 3166-1 alpha-2 country code."""
        return self._country

    @property
    def email(self) -> Optional[str]:
        """The user’s email address, as entered by the user when creating their account."""
        return self._email

    @property
    def product(self) -> Optional[str]:
        """The user’s Spotify subscription level: “premium”, “free”/"open", etc."""
        return self._product
