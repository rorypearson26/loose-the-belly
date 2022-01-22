"""Module to contain `Weight` class."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

import app.utilities.helper_functions as utils


Base = declarative_base()


class Weight(Base):
    """Class to contain attributes needed associated to a weight measurement."""

    __tablename__ = "weights"
    id = Column(
        Integer,
        primary_key=True,
    )
    weight = Column(Float)
    date = Column(DateTime, default=datetime.now())
    clothing_code = Column(String, default="l")

    def __init__(self, weight, clothing_code, date):
        """Initialise Weight object.

        Args:
            weight (int): [description]
            clothing_code (str): [description]
            date (str, optional): [description]. Defaults to datetime.now().
        """

        self.weight = float(weight)
        self.clothing_code = clothing_code
        self.date = self.parse_date(date)

    def parse_date(self, date):
        if date is False:
            date = datetime.now()
        else:
            date = utils.format_dates(date=date, date_format="%d-%m-%y")
        return date

    def parse_clothing_code(self, clothing_code):
        if clothing_code is False:
            clothing_code = "l"
        else:
            clothing_code = clothing_code
        return clothing_code
