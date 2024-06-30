#!/usr/bin/python3

"""defines the class DB_Storage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
import models
from base_model import Base


class DBStorage:
    """manages hbnb models in MySQL database"""

    __engine = None
    __session = None

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

        # create all tables in database
        Base.metadata.create_all(self.__engine)

        # create class for making sessions
        session_build = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # create new session (scoped)
        self.__session = scoped_session(session_build)


    # FIXME
    def all(self, cls=None):
        """query all objects of specified class

        if no class is specified, all objects of all classes are queried
        """

        from models import class_lookup

        query_dict = {}

        # first check that cls is not None
        if cls:
            # convert cls to class from string
            if type(cls) is str:
                cls = class_lookup.get(cls, None)
            for obj in self.__session.query(cls):

        else:
            #if cls is None, convert cls to list of all classes
            cls = class_lookup.values()


    def new(self, obj):
        """adds specified object to current database session"""
        # asdf

    def save(self):
        """commit all changes of the current database session"""
        # asdf

    def delete(self, obj=None):
        """deletes obj from the current database session if not None"""
        # asdf

    def reload(self):
        """creates all tables in the database

        also creates current database session
        """
        # asdf


#     Base.metadata.create_all(bind=engine)
#
#     Session = sessionmaker(bind=engine)
#
#     with Session() as session:
#         place = session.query(City, State).join(State).order_by(City.id).all()
#         for city, state in place:
#             print(f"{state.name}: ({city.id}) {city.name}")
#
#
# if __name__ == "__main__":
#     model_city_fetch_by_state()
