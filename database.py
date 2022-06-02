# url_shortener/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# NOTE: the "declarative base" function returns a class that connects
# the database engine to the SQLAlchemy functionality of the models.
# We assign declarative_base() to Base in which it will inherit the
# database model from our models.py file
Base = declarative_base()