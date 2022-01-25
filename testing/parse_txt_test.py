"""Class for testing `helper_functions.parse_txt` function."""

import unittest
from unittest.mock import MagicMock

from app.utilities.helper_functions import TextParser

parse_test = TextParser.parse_txt


class ParseTxtTestModule(unittest.TestCase):
    """Test the function `helper_functions.parse_txt`."""

    def setUp(self):
        self.weight_regex = self.retrieve_regex("weight")
        self.date_regex = self.retrieve_regex("date")
        self.clothing_code_regex = self.retrieve_regex("clothing_code")

    @staticmethod
    def set_up_mock(regex, input_text, cast_to_type=str):
        mock = MagicMock()
        mock.regex = regex
        mock.input_text = input_text
        mock.cast_to_type = cast_to_type
        return mock

    @staticmethod
    def retrieve_regex(regex_name):
        mock = MagicMock()
        mock.regex_name = regex_name
        regex = TextParser.get_regex(mock)
        return regex

    def test_returns_false_when_not_matched_using_date_regex(self):
        input_strings = [
            "No date in format %d-%m-%y here",
            "20-1-19",
            "1-1-2000",
            "20/11/21",
        ]
        self.false_test(input_strings, self.date_regex)

    def test_returns_false_when_not_matched_using_clothing_code_regex(self):
        input_strings = [
            "no clothing code here",
            "nhl hl nh",
            "19-20-18n",
            "19-20-18n",
            "19-20-18n",
        ]
        self.false_test(input_strings, self.clothing_code_regex)

    def test_returns_false_when_not_matched_using_weight_regex(self):
        input_strings = ["100.0fs", "not a number", "80df", "20-19-22"]
        self.false_test(input_strings, self.weight_regex)

    def test_returns_expected_match_using_weight_regex(self):
        input_output_dict = {
            "11": "add 11 this",
            "12.4": "add 12.4",
            "13": "add 13",
            "14.5": "add 14.5 n",
        }
        self.true_test(input_output_dict, self.weight_regex)

    def test_returns_expected_match_using_date_regex(self):
        input_output_dict = {
            "11-12-22": "add 11 this 11-12-22",
            "12-12-22": "add 11 this 12-12-22 n",
        }
        self.true_test(input_output_dict, self.date_regex)

    def test_returns_expected_match_using_clothing_code_regex(self):
        input_output_dict = {
            "n": "add 11 11-12-22 n",
            "l": "add 11 12-12-22 l",
            "h": "add 11 12-12-22 h",
        }
        self.true_test(input_output_dict, self.clothing_code_regex)

    def false_test(self, input_strings, regex):
        for test_str in input_strings:
            mock = self.set_up_mock(regex=regex, input_text=test_str)
            func_result = TextParser.parse_txt(mock)
            with self.subTest(f"{test_str} should return `False`"):
                self.assertFalse(func_result)

    def true_test(self, input_output_dict, regex):
        for expected, test_str in input_output_dict.items():
            mock = self.set_up_mock(regex=regex, input_text=test_str)
            func_result = TextParser.parse_txt(mock)
            with self.subTest(f"`{test_str}` should return `{expected}`"):
                self.assertEqual(expected, func_result)


if __name__ == "__main__":
    unittest.main(verbosity=1)
