"""Module to contain general helper functions to keep `app.py` uncluttered.

Will probably come back later and refactor into different modules.
"""
import re


def get_weight(message_str):
    """Strip the weight from the passed in string and cast to float.

    Args:
        message_str (str): String received from Slack.

    Returns:
        (bool or float): `False` if no match found. However, if a match is found it will be
        returned and cast to `float`.
    """
    kg_regex = r"\d+.\d+|\d+"
    match = re.search(kg_regex, message_str)
    if match:
        return round(float(match[0]), 2)
    else:
        return False
