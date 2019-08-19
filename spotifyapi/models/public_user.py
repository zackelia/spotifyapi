"""Provide the public user model."""
from .user import User


class PublicUser(User):
    """Public user profile"""

    def __init__(self, data):
        super().__init__(data)
