#!/usr/bin/env python3
""" Basic auth
"""

from .auth import Auth


class BasicAuth(Auth):
    """ empty class
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
            ) -> str:
        """ returns a base64 aprt of Auth headers
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
            )-> str:
        """ returns the decoded valueof Base64 str
        """
        
