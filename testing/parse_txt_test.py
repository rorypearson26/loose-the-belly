"""Class for testing `helper_functions.parse_txt` function."""

import re
import unittest

from app.utilities.helper_functions import parse_txt


class ParseTxtTestModule(unittest.TestCase):
    """Test the function `helper_functions.parse_txt`."""

    def setUp(self):
        self.regex_string_dict = {
            "weight": r"\d+.\d+|\d+",
            "date": r"(?<= )\d{2}-\d{2}-\d{2}",
            "clothing_code": r"(?<= )[n|h|l](?= )",
        }

    def test_returns_false_when_not_matched_using_date_regex(self):
        regex = self.regex_string_dict["date"]
        input_strings = [
            "No date in format %d-%m-%y here",
            "20-1-19",
            "1-1-2000",
            "20/11/21",
        ]
        for test in input_strings:
            func_result = parse_txt(test, regex)
            with self.subTest(f"{test} should return `False`"):
                self.assertFalse(func_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
