#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ class manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]
                     ) -> bool:
        """ returns false
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ return None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None
        """
        return None
