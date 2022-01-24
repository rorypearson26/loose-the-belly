"""Class for testing `helper_functions.parse_txt` function."""

import unittest

from app.utilities.helper_functions import parse_txt


class ParseTxtTestModule(unittest.TestCase):
    """Test the function `helper_functions.parse_txt`."""

    def setUp(self):
        self.regex_string_dict = {
            "weight": r"(?<= )\d+.\d+|\d+(?= )",
            "date": r"(?<= )\d{2}-\d{2}-\d{2}(?= )",
            "clothing_code": r"(?<= )[n|h|l](?= )",
        }

    def test_returns_false_when_not_matched_using_date_regex(self):
        input_strings = [
            "No date in format %d-%m-%y here",
            "20-1-19",
            "1-1-2000",
            "20/11/21",
        ]
        self.false_test(input_strings, "date")

    def test_returns_false_when_not_matched_using_clothing_code_regex(self):
        input_strings = ["no clothing code here", "nhl hl nh", "n ", "h", "l"]
        self.false_test(input_strings, "clothing_code")

    def test_returns_false_when_not_matched_using_weight_regex(self):
        input_strings = ["100.0fs", "not a number", "80df"]
        self.false_test(input_strings, "weight")

    def test_returns_expected_match_using_weight_regex(self):
        input_output_dict = {
            "11": "add 11 this",
            "12.4": "add 12.4",
            "13": "add 13",
            "14.5": "add 14.5 n",
        }
        self.true_test(input_output_dict, "weight")

    def test_returns_expected_match_using_date_regex(self):
        input_output_dict = {
            "11-12-22": "add 11 this 11-12-22",
            "12-12-22": "add 11 this 12-12-22 n",
        }
        self.true_test(input_output_dict, "date")

    def test_returns_expected_match_using_clothing_code_regex(self):
        input_output_dict = {
            "n": "add 11 11-12-22 n",
            "l": "add 11 12-12-22 l",
            "h": "add 11 12-12-22 h",
        }
        self.true_test(input_output_dict, "clothing_code")

    def false_test(self, input_strings, regex_type):
        regex = self.regex_string_dict[regex_type]
        for test in input_strings:
            func_result = parse_txt(test, regex)
            with self.subTest(f"{test} should return `False`"):
                self.assertFalse(func_result)

    def true_test(self, input_output_dict, regex_type):
        regex = self.regex_string_dict[regex_type]
        for expected, input_str in input_output_dict.items():
            func_result = parse_txt(input_str, regex)
            with self.subTest(f"`{input_str}` should return `{expected}`"):
                self.assertEqual(expected, func_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
