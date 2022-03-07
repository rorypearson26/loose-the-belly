from datetime import date, datetime, timedelta


def format_dates(date, date_format=None, return_date_format=None):
    """Converts date string in specified format.
    Args:
        date (str or datetime.datetime): date in string form to convert.
        date_format (str): Date format expected from user.
            See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes for syntax.
        return_date_format (str, optional): Specify string format to return
            date in - if not specified a datetime.datetime will be returned.
    Returns:
        date (datetime.datetime or str): date as a datetime object by default.
            Alternatively a properly formatted date string according
            return_date_format.
    """
    if not isinstance(date, datetime):
        date = datetime.strptime(date, date_format)
    if return_date_format:
        date = date.strftime(return_date_format)
    return date


def get_date_range(length):
    """Returns a tuple of `datetime` objects equivalent to today minus length (months).

    Args:
        length (:obj:`int`): Length in months to go back in time.

    Returns:
        (:obj:`datetime.datetime`, :obj:`datetime.datetime`): Tuple in the format:
        (`start`, `end`).
    """
    end = datetime.now()
    rough_days = int(length) * 30
    start = end - timedelta(days=rough_days)
    return (start, end)
