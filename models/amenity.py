#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models import UsingStorage
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import UsingStorage


class Amenity(BaseModel):
        
    if UsingStorage.DB_STORAGE:
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
