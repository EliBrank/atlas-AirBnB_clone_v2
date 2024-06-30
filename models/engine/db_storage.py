#!/usr/bin/python3

"""defines the class DB_Storage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

        db_url = 'mysql+mysqldb://{}:{}@{}:3306/{}'

        self.__engine = create_engine(
            db_url.format(user, password, host_name, db_name),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

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
