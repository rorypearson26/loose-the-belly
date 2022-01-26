"""Module to keep all database functionality in one place."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.utilities.weight import Weight

DATABASE_NAME = "app/weights.db"


def get_engine():
    return create_engine(f"sqlite:///{DATABASE_NAME}")


def get_session():
    engine = get_engine()
    return sessionmaker(engine)


def initialise_database(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
        Weight.__table__.create(engine)


def add_measurement(weight_obj):
    """Adds weight measurement coming from the slack app to `Weight` table.

    Args:
        weight_obj (:py:class:`Weight`): custom class that contains data needed
            to add a new weight measurement.
    """
    Session = get_session()
    with Session.begin() as s:
        s.add(weight_obj)


def remove_last_measurement():
    """Removes the last measurement added to the database.

    If no measurements exist then `False` is returned.
    """
    Session = get_session()
    with Session.begin() as s:
        last_record = s.query(Weight).order_by(Weight.id.desc()).first()
        result = False if last_record is None else last_record
        s.commit()
        print(result)
        return result


if __name__ == "__main__":
    remove_last_measurement()
