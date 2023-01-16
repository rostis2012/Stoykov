import unittest
# import main

from unittest.mock import patch
from pathlib import Path
from main import parsing_data_to_dict
from main import parsing_data_to_list
from main import make_person_info
from main import read_files
from main import my_main


# class TestReadFiles(unittest.TestCase):
#     def test_exeption(self):
#         with self.assertRaises(FileNotFoundError):
#             read_files('temp_dir')
#
#
# class TestParsingFileToDict(unittest.TestCase):
#     def setUp(self) -> None:
#         self.test_data = ['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6 | БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ']
#         self.expected_result = {'052XL7D4': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6': 'БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ'}
#
#     def test_normal_behavior(self):
#         self.assertEqual(parsing_data_to_dict(self.test_data), self.expected_result)
#
#
# class TestParsingFileToList(unittest.TestCase):
#     def setUp(self) -> None:
#         self.test_data = ['FQPN6GBZ | 2020-01-01 08:11:52',
#                           '9GNOKQJY | 2020-01-01 08:28:55',
#                           'ANTJQK2S | 2020-01-01 08:36:54',
#                           'U9OJVYGQ | 2020-01-01 08:44:52'
#                           ]
#         self.expected_result = [('9GNOKQJY', '2020-01-01', '08:28:55'),
#                                 ('ANTJQK2S', '2020-01-01', '08:36:54'),
#                                 ('FQPN6GBZ', '2020-01-01', '08:11:52'),
#                                 ('U9OJVYGQ', '2020-01-01', '08:44:52')
#                                 ]
#
#     def test_normal_behavior(self):
#         self.assertEqual(parsing_data_to_list(self.test_data), self.expected_result)
#
#
# class TestMakePersonInfo(unittest.TestCase):
#     def setUp(self) -> None:
#         self.person_id = '052XL7D4'
#         self.enter = [('052XL7D4', '2020-01-01', '08:55:54'),
#                       ('052XL7D4', '2020-01-01', '14:29:07'),
#                       ('052XL7D4', '2020-01-02', '08:41:46'),
#                       ('052XL7D4', '2020-01-02', '13:31:44')]
#         self.exit = [('052XL7D4', '2020-01-01', '13:28:18'),
#                      ('052XL7D4', '2020-01-01', '18:10:02'),
#                      ('052XL7D4', '2020-01-02', '13:11:16'),
#                      ('052XL7D4', '2020-01-02', '18:15:01')]
#         self.expected_result = {'2020-01-01': [['08:55:54', '13:28:18'], ['14:29:07', '18:10:02']],
#                                 '2020-01-02': [['08:41:46', '13:11:16'], ['13:31:44', '18:15:01']]}
#
#     def test_normal_behavior(self):
#         self.assertEqual(make_person_info(self.person_id, self.enter, self.exit), self.expected_result)
#

class TestMyMain(unittest.TestCase):
    def setUp(self) -> None:
        self.passed_pass = 'test/path'
        self.read_lines = (['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ\n'],
                           ['052XL7D4 | 2020-01-01 08:55:54 \n',  '052XL7D4 | 2020-01-01 14:29:07 \n'],
                           ['052XL7D4 | 2020-01-01 13:28:18 \n',  '052XL7D4 | 2020-01-01 18:10:02 \n'])
        self.expected_value = {'052XL7D4': {'name': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ',
              'visits': {'2020-01-01': [['08:55:54', '13:28:18'], ['14:29:07', '18:10:02']]}}}

    @patch('Stoykov.diploma.main.read_files')
    def test_normal_behavior(self, mock_read_files):
        mock_read_files.return_value = self.read_lines
        # my_main(self.passed_pass)
        res = my_main(self.passed_pass)
        self.assertEqual(res, self.expected_value)

    # def test_raise_exeption(self):
    #     with self.assertRaises(TypeError):
    #         read_files(444)


if __name__ == '__main__':
    unittest.main()
