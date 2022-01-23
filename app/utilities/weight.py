"""Module to contain `Weight` class."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

from app.utilities.helper_functions import parse_txt, format_dates


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

    def __init__(self, msg_str):
        """Initialise Weight object.

        Args:
            msg_str (str): String coming from picked up slack message.
        """

        self.weight = self.parse_weight(msg_str)
        self.clothing_code = self.parse_clothing_code(msg_str)
        self.date = self.parse_date(msg_str)

    def parse_weight(self, msg_str):
        weight = parse_txt(
            msg_str=msg_str, regex=r"(?<= )\d+.\d+|\d+(?= )", cast_to=float
        )
        if weight is False:
            raise ValueError("Weight could not be parsed.")
        return weight

    def parse_date(self, msg_str):
        date = parse_txt(msg_str=msg_str, regex=r"(?<= )\d{2}-\d{2}-\d{2}(?= )")
        if date is False:
            date = datetime.now()
        else:
            date = format_dates(date=date, date_format="%d-%m-%y")
        return date

    def parse_clothing_code(self, msg_str):
        clothing_code = parse_txt(msg_str=msg_str, regex=r"(?<= )[n|h|l](?= )")
        if clothing_code is False:
            clothing_code = "l"
        else:
            clothing_code = clothing_code
        return clothing_code
