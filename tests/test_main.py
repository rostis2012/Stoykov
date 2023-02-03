import unittest

from Stoykov.src.staff_visits.main import parsing_data_to_dict


class TestParsingFileToDict(unittest.TestCase):
    def setUp(self):
        self.test_data = ['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6 | БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ']
        self.expected_result = {'052XL7D4': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ', '5OALCRB6': 'БОНДАРЕНКО ВАСИЛЬ ІВАНОВИЧ'}

    def test_normal_behavior(self):
        self.assertEqual(parsing_data_to_dict(self.test_data), self.expected_result)


if __name__ == '__main__':
    unittest.main()
