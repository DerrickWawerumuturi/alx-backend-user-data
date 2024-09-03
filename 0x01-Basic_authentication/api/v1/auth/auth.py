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
        """ checks if a path should be excluded from
        authentication
        """
        if not path:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        slashed_path = path if path.endswith('/') else path + "/"

        for excluded in excluded_paths:
            if slashed_path == excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ return None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None
        """
        return None
