"""Module to contain general helper functions to keep `app.py` uncluttered.

Will probably come back later and refactor into different modules.
"""
from datetime import datetime
import re

from app.utilities.weight import Weight


def parse_txt(msg_str, regex, cast_to=str):
    """Strip required section of text based on regex and cast to specified type.

    Args:
        msg_str (str): String received from Slack.
        regex (str): Regex that will be used to search for section in message.
        cast_to (type): data type that the match is to be cast to.

    Returns:
        (bool or float): `False` if no match found. However, if a match is found it will be
        returned and cast to specified type.
    """
    match = re.search(regex, msg_str)
    if match:
        return cast_to(match[0])
    else:
        return False


def parse_measurement(msg_str):
    """Parse string coming from slack into a useable format.

    Args:
        msg_str (str): String coming from picked up slack message.

    Returns:
        weight_obj (Weight): Object containing data needed to add measurement record to database.
    """
    weight = parse_txt(msg_str=msg_str, regex=r"(?<= )\d+.\d+|\d+(?= )", cast_to=float)
    if weight:
        clothing_code = parse_txt(msg_str=msg_str, regex=r"(?<= )[n|h|l](?= )")
        date = parse_txt(msg_str=msg_str, regex=r"(?<= )\d{2}-\d{2}-\d{2}(?= )")
        weight_obj = Weight(weight=weight, clothing_code=clothing_code, date=date)
        return weight_obj
    else:
        return False


def format_dates(date, date_format=None, return_date_format=None):
    """Converts date string in specified format.
    Args:
        date (str or datetime.datetime): date in string form to convert.
        date_format (str): Date format expected from user.
            See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes for syntax.
        return_date_format (str, optional): Specify string format to return date in - if not
            specified a datetime.datetime will be returned.
    Returns:
        date (datetime.datetime or str): date as a datetime object by default. Alternatively a
            properly formatted date string according to return_date_format.
    """
    try:
        if not isinstance(date, datetime.datetime):
            date = datetime.datetime.strptime(date, date_format)
        if return_date_format:
            date = date.strftime(return_date_format)
        return date
    except ValueError:
        print(f"Variable `date_format`: {date} should be in the format {date_format}.")
