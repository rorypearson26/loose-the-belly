"""Module to contain `Weight` class."""
from datetime import datetime


class Weight:
    """[summary]"""

    def __init__(self, weight, clothing_code="l", date=datetime.now()):
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
        if isinstance()
