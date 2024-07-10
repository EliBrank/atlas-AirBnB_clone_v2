#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all")
        reviews = relationship("Review", backref="user", cascade="all")
        # backref creates a bidirectional relationship by automatically
        # creating an attribute in the related class
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
