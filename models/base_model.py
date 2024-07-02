#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid, models
from os import getenv

# used for formatting datetime elements with strptime
time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

# checks storage engine (db_storage vs file_storage)
if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        # passed in key/value pairs can define object attributes
        for key, value in kwargs.items():
            # can't redefine class, however
            if key != '__class__':
                setattr(self, key, value)

        if type(self.created_at) is str:
            self.created_at = datetime.strptime(self.created_at, time_fmt)
        if type(self.updated_at) is str:
            self.updated_at = datetime.strptime(self.updated_at, time_fmt)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if "sa_instance_state" in dictionary:
            dictionary.pop("sa_instance_state", None)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
        # """returns a dictionary containing all keys/values of the instance"""
        # new_dict = self.__dict__.copy()
        # if "created_at" in new_dict:
        #     new_dict["created_at"] = new_dict["created_at"].isoformat()
        # if "updated_at" in new_dict:
        #     new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        # if '_password' in new_dict:
        #     new_dict['password'] = new_dict['_password']
        #     new_dict.pop('_password', None)
        # if 'amenities' in new_dict:
        #     new_dict.pop('amenities', None)
        # if 'reviews' in new_dict:
        #     new_dict.pop('reviews', None)
        # if 'sa_instance_state' in new_dict:
        # new_dict["__class__"] = self.__class__.__name__
        # new_dict.pop('_sa_instance_state', None)
        # if not save_to_disk:
        #     new_dict.pop('password', None)
        # return new_dict

    def delete(self):
        """Deletes current instance from storage"""
        models.storage.delete(self)
