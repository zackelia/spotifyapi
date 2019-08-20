"""Provide the decorators module."""
import requests

from ..exceptions import InvalidScopeError


def scope(*scopes):
    """Decorator for calls that require scope."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except requests.exceptions.HTTPError as e:
                # Check for Client Error 401 Unauthorized
                if e.response.status_code == 401:
                    raise InvalidScopeError(
                        f"{func.__qualname__} requires: {[s for s in scopes]}"
                    )
                raise

        return wrapper

    return decorator
