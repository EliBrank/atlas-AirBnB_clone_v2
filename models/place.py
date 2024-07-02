#!/usr/bin/python3
""" Place Module for HBNB project """
from models import UsingStorage
from models.base_model import BaseModel, Base
import models
import sqlalchemy
import os
from sqlalchemy import Column, Float, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


if UsingStorage.DB_STORAGE:
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))

# onupdate and ondelete are options used in database 
# schema definitions, particularly when defining 
# relationships between tables. These options specify 
# what actions should be taken on related rows when 
# the rows in the referenced table are updated or deleted.
# Cascade update the foreign key when the row is updated
# or deleted.

class Place(BaseModel):
    """ A place to stay """

    if UsingStorage.DB_STORAGE:
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", 
                                 secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []
        amenities = []
        reviews = []

        @property
        def reviews(self):
            """returns a list of reviews"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """returns a list of amenities"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
