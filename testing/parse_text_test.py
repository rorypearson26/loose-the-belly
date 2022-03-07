"""Class for testing `helper_functions.parse_text` function."""

import unittest
from unittest.mock import MagicMock

from app.utilities.helper_functions import TextParser

parse_test = TextParser.parse_text


class ParseTextTestModule(unittest.TestCase):
    """Test the function `helper_functions.parse_text`.

    At the point where this function is called, all text will be in lowercase.
    """

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
            "add 20-1-19",
            "add 112000",
            "add 20/11/21",
            "add 401221",
        ]
        self.false_test(input_strings, self.date_regex)

    def test_returns_false_when_not_matched_using_clothing_code_regex(self):
        input_strings = [
            "no clothing code here",
            "nhl hl nh",
            "192018n",
            "192018n",
            "192018n",
        ]
        self.false_test(input_strings, self.clothing_code_regex)

    def test_returns_false_when_not_matched_using_weight_regex(self):
        input_strings = ["100.0fs", "not a number", "80df", "201922"]
        self.false_test(input_strings, self.weight_regex)

    def test_returns_expected_match_using_weight_regex(self):
        input_output_dict = {
            "11.4": "add 11.4 this",
            "12.4": "add 12.4",
            "13.0": "add 13.0",
            "14.5": "add 14.5 n",
        }
        self.true_test(input_output_dict, self.weight_regex)

    def test_returns_expected_match_using_date_regex(self):
        input_output_dict = {
            "111222": "add 11 this 111222",
            "121222": "add 11 this 121222 n",
        }
        self.true_test(input_output_dict, self.date_regex)

    def test_returns_expected_match_using_clothing_code_regex(self):
        input_output_dict = {
            "n": "add 70.2 n 071221",
            "l": "add 11 121222 l",
            "h": "add 11 121222 h",
        }
        self.true_test(input_output_dict, self.clothing_code_regex)

    def false_test(self, input_strings, regex):
        for test_str in input_strings:
            mock = self.set_up_mock(regex=regex, input_text=test_str)
            func_result = TextParser.parse_text(mock)
            with self.subTest(f"{test_str} should return `False`"):
                self.assertFalse(func_result)

    def true_test(self, input_output_dict, regex):
        for expected, test_str in input_output_dict.items():
            mock = self.set_up_mock(regex=regex, input_text=test_str)
            func_result = TextParser.parse_text(mock)
            with self.subTest(f"`{test_str}` should return `{expected}`"):
                self.assertEqual(expected, func_result)


if __name__ == "__main__":
    unittest.main(verbosity=1)
