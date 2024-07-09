#!/usr/bin/python3
"""instantiates an object of class FileStorage or DBStorage"""
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()


def get_class_lookup():
    """defines dictionary of classes with string counterparts"""

    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    return {
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }


# this dictionary is used to convert between strings and classes
# import using "from models import class_lookup"
class_lookup = get_class_lookup()
