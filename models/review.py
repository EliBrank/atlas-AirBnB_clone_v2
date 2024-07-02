#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import UsingStorage


class Review(BaseModel):
    """ Review class to store review information """
    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
