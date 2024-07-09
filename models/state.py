#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class State(BaseModel, Base):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            backref='state',
            cascade='all'
        )
    else:
        name = ""

        @property
        def cities(self):
            """getter attribute for cities"""

            from models import storage
            from models.city import City

            # initialize list to save cities
            city_list = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                # check each city's state_id against those connected to State
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list
