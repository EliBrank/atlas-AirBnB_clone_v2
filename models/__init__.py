#!/usr/bin/python3
"""instantiates an object of class FileStorage or DBStorage"""
from enum import Enum
from os import getenv


class StorageType(Enum):
    """creates enum DB to check if using database storage"""
    DB = getenv('HBNB_TYPE_STORAGE') == 'db'

if StorageType.DB:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
