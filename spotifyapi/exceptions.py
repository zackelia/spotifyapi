"""Provide custom exceptions"""


class ExpiredTokenError(Exception):
    """Exception when an access token is no longer valid."""


class InvalidScopeError(Exception):
    """Exception when a method is called without the proper scope."""


class SpotifyAPIError(Exception):
    """Generic error from an endpoint."""
