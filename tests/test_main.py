import unittest

# from unittest.mock import patch

from Stoykov.src.staff_visits.main import parsing_data_to_dict
# from Stoykov.src.staff_visits.main import main


class TestParsingFileToDict(unittest.TestCase):
    def setUp(self):
        self.test_data = ['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6 | БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ']
        self.expected_result = {'052XL7D4': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6': 'БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ'}

    def test_normal_behavior(self):
        self.assertEqual(parsing_data_to_dict(self.test_data), self.expected_result)


# class TestMain(unittest.TestCase):
#     def setUp(self):
#         self.passed_pass = 'test/path'
#         self.read_lines = (['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ\n'],
#                            ['052XL7D4 | 2020-01-01 08:55:54 \n',  '052XL7D4 | 2020-01-01 14:29:07 \n'],
#                            ['052XL7D4 | 2020-01-01 13:28:18 \n',  '052XL7D4 | 2020-01-01 18:10:02 \n'])
#         self.expected_value = {'052XL7D4': {'name': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ',
#               'visits': {'2020-01-01': [['08:55:54', '13:28:18'], ['14:29:07', '18:10:02']]}}}
#
#     @patch('Stoykov.src.staff_visits.main.read_files')
#     def test_normal_behavior(self, mock_read_files):
#         mock_read_files.return_value = self.read_lines
#         self.assertEqual(main(self.passed_pass), self.expected_value)


if __name__ == '__main__':
    unittest.main()
