"""
WSGI middleware for the web app
"""

import hashlib
import os
from typing import Callable, Dict, Iterable

class AuthMiddleware:
    """
    WSGI middleware to check that the X-Token request header is correct.
    """

    def __init__(self, app: Callable):
        """
        Args:
            app: the WSGI app to wrap
        """
        self.app = app
        # Hashing to help prevent timing attacks
        self._token_digest = self._digest(
            os.environ.get('REMOTE_SCREEN_LOCKER_TOKEN', '')
        )

    def __call__(
            self,
            environ: Dict[str, object],
            start_response: Callable,
    ) -> Iterable[bytes]:
        """Checks the X-Token request header.

        If the token in the header is correct, this will proceeed. Otherwise,
        it will respond with a 401.

        Args:
            environ: CGI environment variables
            start_response: callable to begin the HTTP response
        """
        if self._digest(environ.get('HTTP_X_TOKEN', '')) == self._token_digest:
            return self.app(environ, start_response)
        else:
            start_response('401 Unauthorized', [])
            return []

    @staticmethod
    def _digest(s: str) -> bytes:
        """Hashes a given string.

        Args:
            s: the string to hash
        Returns:
            the digest as bytes
        """
        return hashlib.sha256(s.encode()).digest()
