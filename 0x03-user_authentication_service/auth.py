#!/usr/bin/env python3
""" Hash password
"""

from db import DB
from user import User
import bcrypt
from typing import Union
from sqlalchemy.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ hashes a password
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False
        return False

    def _generate_uuid(self) -> str:
        """ Generate UUIDs
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """ Gets session id
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """ Finds user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """ destroys a users session Id
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generate reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        newToken = self._generate_uuid()
        self._db.update_user(user.id, reset_token=newToken)
        return newToken

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_pwd = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_pwd,
            reset_token=None
        )
