"""Module to contain general helper functions to keep `app.py` uncluttered.

Will probably come back later and refactor into different modules.
"""
import re


class TextParser:
    def __init__(self, input_text, regex_name, cast_to_type=str):
        """Initialise `TextParser` class.

        Args:
            input_text (str): String received from Slack.
            regex_name (str): name of regex to use for parsing.
            cast_to_type (type): data type that the match is to be cast to.
        """
        self.input_text = input_text.lower()
        self.regex_name = regex_name
        self.cast_to_type = cast_to_type
        self.regex = self.get_regex()
        self.parsed_text = self.parse_text()
        self.valid = True if self.parsed_text else False

    def get_regex(self):
        """Retrieve the regex corresponding to `self.regex_name`.

        Returns:
            regex (str): Predefined regex corresponding to `self.regex_name`.
        """
        regex_dict = {
            "weight": r"(?:(?<=\s)|^)\d+\.\d+(?=\s|$)",
            "date": r"(?<= )[0-3][0-9](?:0[1-9]|1[0-2])[1-2][0-9](?=\s|$)",
            "clothing_code": r"(?<= )[n{1}|h{1}|l{1}](?=\s|$)",
            "time": r"(?<= )[0-2][0-9][0-5][0-9](?=\s|$)"
        }
        regex = regex_dict[self.regex_name]
        return regex

    def parse_text(self):
        """Strip required section of text based on regex and specified type to cast to.

        Returns:
            match or bool: `False` if no match found. However, if a match is found
                will be returned and cast to specified type.
        """
        match = re.search(self.regex, self.input_text, flags=re.IGNORECASE)
        if match:
            return self.cast_to_type(match[0])
        else:
            return False
