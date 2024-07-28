import unittest
from unittest.mock import mock_open, patch
import re
from gemini.helper import read_text_from_file, parse_response_to_json

class TestHelperFunctions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="This is a test prompt.")
    def test_read_text_from_file(self, mock_file):
        file_path = 'dummy_path.txt'
        expected_content = "This is a test prompt."

        content = read_text_from_file(file_path)

        self.assertEqual(content, expected_content)
        mock_file.assert_called_once_with(file_path, 'r', encoding="utf-8")

    def test_parse_response_to_json_success(self):
        response = "1. Key1: Value1\n2. Key2: Value2\n3. Key3: Value3\n"
        expected_json = {
            "key1": "Value",
            "key2": "Value2",
            "key3": "Value3"
        }

        result_json = parse_response_to_json(response)

        self.assertEqual(result_json, expected_json)

    def test_parse_response_to_json_malformed(self):
        response = "This is not a properly formatted response."
        expected_json = {
            "error": "Not an image of a living organism (plant, insect or animal)",
            "next_steps": "Insert a clear image of a plant, insect, or animal and try again."
        }

        result_json = parse_response_to_json(response)

        self.assertEqual(result_json, expected_json)

    def test_parse_response_to_json_partial_malformed(self):
        response = "1. Key1: Value1\n2. Key2\n3. Key3: Value3\n"
        expected_json = {
            "key1": "Value",
            "key3": "Value3"
        }

        result_json = parse_response_to_json(response)

        self.assertEqual(result_json, expected_json)
