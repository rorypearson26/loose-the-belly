"""Class for testing `weight.Weight.parse_date` function."""

import unittest
from unittest.mock import Mock
from datetime import datetime

from app.utilities.weight import Weight

parse_date = Weight.parse_date


class ParseDateTestModule(unittest.TestCase):
    """Test the function `weight.Weight.parse_date`.

    At the point where this function is called, all text will be in lowercase.
    """

    def setUp(self):
        self.Mock = Mock

    def test_returns_correct_datetime_when_using_both_time_and_date(self):
        date_format = '%d%m%y%H%M'
        input_strings = [
            "filler 0230 120222",
            "filler 1830 190521",
            "filler 1201 300119",
            "filler 020212 1202",
            "filler 250116 2236",
            "filler 070322 0751"
        ]
        expected_output = [
            datetime.strptime('1202220230', date_format),
            datetime.strptime('1905211830', date_format),
            datetime.strptime('3001191201', date_format),
            datetime.strptime('0202121202', date_format),
            datetime.strptime('2501162236', date_format),
            datetime.strptime('0703220751', date_format)
        ]
        for i, test_str in enumerate(input_strings):
            with self.subTest(test_str):
                func_result = parse_date(self.Mock, test_str)
                self.assertEqual(func_result, expected_output[i])
