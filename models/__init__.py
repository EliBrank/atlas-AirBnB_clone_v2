#!/usr/bin/python3
"""instantiates an object of class FileStorage or DBStorage"""
from enum import Enum
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# this dictionary is used to convert between strings and classes
# import using "from models import class_lookup"
class_lookup = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review
}


# sets up enum to check if using DBStorage
# import using "from models import UsingStorage"
class UsingStorage(Enum):
    """creates enum DB to check if using database storage"""
    # if the env var is set to 'db' then DB_STORAGE will evaluate to true
    DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'


if UsingStorage.DB_STORAGE:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
