"""Module to keep all database functionality in one place."""
from datetime import datetime
import time

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
    engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
DATABASE_NAME = "app/weights.db"
engine = create_engine(f"sqlite:///{DATABASE_NAME}")
Session = sessionmaker(engine)


def initialise_database():
    if not database_exists(engine.url):
        create_database(engine.url)
        time.sleep(3)
        Weight.__table__.create(engine)


class Weight(Base):
    __tablename__ = "weights"
    id = Column(
        Integer,
        primary_key=True,
    )
    weight = Column(Float)
    date = Column(DateTime, default=datetime.now())
    clothing_code = Column(String, default="l")


def add_measurement(weight, clothing_code, date=datetime.now()):
    """Adds weight measurement coming from the slack app to `Weight` table.

    Args:
        weight (float): [description]
        clothing_code (str) [description]
        date (datetime, optional): Date measurement was recorded. Defaults to current datetime.
    """
    measurement = Weight(weight=weight, date=date, clothing_code=clothing_code)
    with Session() as s:
        s.add(measurement)
        s.commit()
