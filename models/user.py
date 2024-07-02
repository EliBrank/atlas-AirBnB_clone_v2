#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
from os import getenv
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class User(BaseModel):
    """This class defines a user"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
        # backref creates a bidirectional relationship by
        # automatically creating an attribute in the related
        # class
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
