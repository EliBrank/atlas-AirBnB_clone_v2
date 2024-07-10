#!/usr/bin/python3

from sqlalchemy import create_engine
from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base, BaseModel

user = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host_name = getenv('HBNB_MYSQL_HOST')
db_name = getenv('HBNB_MYSQL_DB')
env = getenv('HBNB_ENV')

db_url = 'mysql+mysqldb://{}:{}@{}:3306/{}'

engine = create_engine(
    db_url.format(user, password, host_name, db_name),
    pool_pre_ping=True
)

# Drop all tables
Base.metadata.drop_all(engine)
