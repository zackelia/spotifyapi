"""Provide the decorators module."""
import requests


def scope(*scopes):
    """Decorator for calls that require scope."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except requests.exceptions.HTTPError as e:
                # Check for Client Error 401 Unauthorized
                if e.response.status_code == 401:
                    raise ValueError(
                        f"{func.__qualname__} requires: {[scope for scope in scopes]}"
                    )
                raise

        return wrapper

    return decorator
