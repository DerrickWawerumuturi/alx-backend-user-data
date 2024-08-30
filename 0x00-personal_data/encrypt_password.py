#!/usr/bin/env python3
"""  Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validates password with hash
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
