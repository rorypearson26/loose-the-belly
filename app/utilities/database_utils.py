"""Module to keep all database functionality in one place."""
import sqlite3

from sqlalchemy import (Column, DateTime, Float, Integer, MetaData, String,
                        Table, create_engine, engine)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
DATABASE_NAME = "app/weights.db"
initialise_database()

class Weight(Base):
    __tablename__ = 'weights'
    id = Column(Integer, primary_key=True),
    name = Column(String),
    weight = Column(Float),
    date = Column(DateTime),
    clothing_code = Column(String),
    
def initialise_database():
    meta = MetaData()
    engine = create_engine(f"sqlite:///{DATABASE_NAME}")
    if not database_exists(engine.url):
        create_database(engine.url)
        weights = Table(
            "weights",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("weight", Float),
            Column("date", DateTime),
            Column("clothing_code", String)
        )
        meta.create_all(engine)
    return engine


# def populate_from_csv():


def add_weight_measurement(weight):
    with engine


# if __name__ == "__main__":
#     create_database()
