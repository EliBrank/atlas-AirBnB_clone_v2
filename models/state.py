#!/usr/bin/python3
""" State Module for HBNB project """
from models import UsingStorage
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class State(BaseModel, Base):
    """ State class """
    if UsingStorage.DB_STORAGE:
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            # names reference (within city back to State object) as state
            backref='state',
            # specifies behavior when the instance is deleted
            # 'all' uses all cascade options (delete, delete-orphan, etc.)
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
                # check each city's state_id against those connected to State object
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list
