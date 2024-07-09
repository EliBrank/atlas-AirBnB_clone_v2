#!/usr/bin/python3

"""defines the class DB_Storage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base, BaseModel


class DBStorage:
    """manages hbnb models in MySQL database"""

    __engine = None
    __session: scoped_session = None

    def __init__(self):
        """initializes the storage database"""

        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host_name = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        db_url = 'mysql+mysqldb://{}:{}@{}:3306/{}'

        self.__engine = create_engine(
            db_url.format(user, password, host_name, db_name),
            pool_pre_ping=True
        )

        # drop all tables if using test environment
        if env == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query all objects of specified class

        if no class is specified, all objects of all classes are queried
        """

        from models import class_lookup

        if self.__session is None:
            self.reload()

        objects = {}

        # first check that cls is not None
        if cls:
            # convert cls to class from string (if needed)
            if type(cls) is str:
                cls = class_lookup.get(cls, None)
            objects = self.__session.query(cls).all()
            # dictionary comprehension formats dict as:
            # <class_name>.<object_id> : object
            query_dict = {
                "{}.{}".format(cls.__name__, obj.id) : obj for obj in objects
            }

            return query_dict

        else:
            # if cls is None, combine queries of all classes
            query_dict = {}

            for cls in class_lookup.values():
                objects = self.__session.query(cls).all()

                # update query_dict with new class objects
                query_dict.update({
                    "{}.{}".format(cls.__name__, obj.id): obj for obj in objects
                })

            return query_dict


    def new(self, obj):
        """adds specified object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj from the current database session if not None"""
        self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database

        also creates current database session
        """
        # create all tables in database
        Base.metadata.create_all(self.__engine)

        # create class for making sessions
        session_build = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # create new session (scoped)
        self.__session = scoped_session(session_build)

    def close(self):
        """closes current session"""
        self.__session.remove()
