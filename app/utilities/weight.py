"""Module to contain `Weight` class."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

from app.utilities.helper_functions import (TextParser, format_dates, DateFormatError)


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

    def __repr__(self):
        info = (
            f"weight: {self.weight}, clothing_code: {self.clothing_code}, "
            f"date: {format_dates(date=self.date, return_date_format='%d-%m-%y')}"
        )
        return info

    def parse_weight(self, msg_str):
        weight = TextParser(input_text=msg_str, cast_to_type=float, regex_name="weight")
        if not weight.valid:
            raise ValueError("Weight could not be parsed.")
        return weight.parsed_text

    def parse_date(self, msg_str):
        time = TextParser(input_text=msg_str, regex_name="time")
        date = TextParser(input_text=msg_str, regex_name="date")
        if not date.valid:
            parsed_text = datetime.now()
        else:
            if time:
                date_format = "%d%m%y%H%M"
                text = f"{date.parsed_text}{time.parsed_text}"
            else:
                date_format = "%d%m%y"
                text = date.parsed_text
            parsed_text = format_dates(
                date=text, date_format=date_format
            )
        return parsed_text

    def parse_clothing_code(self, msg_str):
        clothing_code = TextParser(input_text=msg_str, regex_name="clothing_code")
        if not clothing_code.valid:
            clothing_code.parsed_text = "l"
        return clothing_code.parsed_text
