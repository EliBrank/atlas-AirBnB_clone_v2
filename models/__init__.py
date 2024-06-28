#!/usr/bin/python3
"""instantiates an object of class FileStorage or DBStorage"""
from enum import Enum
from os import getenv


class UsingStorage(Enum):
    """creates enum DB to check if using database storage"""
    DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if UsingStorage.DB_STORAGE:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
