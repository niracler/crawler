from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings
import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Movie(DeclarativeBase):
    __tablename__ = "movie"

    mid = Column('mid', Integer, primary_key=True)
    name = Column('name', String(65))
    english_name = Column('english_name', String(128))
    release_year = Column('release_year', String(16))
    default_image = Column('default_image', String(256))
    box_office = Column('box_office', Integer)
    area = Column('area', String(128))
    area_id = Column('area_id', Integer)
    ranking = Column('ranking', Integer)
    style = Column('style', String(64))
    release_time = Column('release_time', String(128))
    duration = Column('duration', String(64))
    movie_type = Column('movie_type', String(64))
    director = Column('director', String(256))
    starring = Column('starring', String(256))
    production_company = Column('production_company', String(256))
    publish_company = Column('publish_company', String(256))
    created = Column('created', DateTime(), default=datetime.datetime.utcnow)


class MovieBoxOffice(DeclarativeBase):
    __tablename__ = "movie_box_office"

    id = Column(Integer, autoincrement=True, primary_key=True)
    mid_id = Column('mid_id', Integer)
    week = Column('week', String(64))
    week_time = Column('week_time', String(128))
    average_per_game = Column('average_per_game', Integer)
    one_week_box_office = Column('one_week_box_office', Integer)
    total_box_office = Column('total_box_office', Integer)
    days_released = Column('days_released', Integer)
