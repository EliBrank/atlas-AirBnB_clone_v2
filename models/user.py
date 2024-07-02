#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import UsingStorage


class User(BaseModel):
    """This class defines a user"""
    if UsingStorage.DB_STORAGE:
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
