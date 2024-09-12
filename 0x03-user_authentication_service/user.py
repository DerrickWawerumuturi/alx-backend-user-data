#!/usr/bin/env python3
"""
User model
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """ model class/ rep a table User in the db
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
