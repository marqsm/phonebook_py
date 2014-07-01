import unittest
import phonebook

class TestPhonebook(Unittest.TestCase):
    def test_pb_parse_input_row(self):
        actual = pb_parse_input_rows('jaska 123456')
        expected = {'jaska': '123456'}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(exit=False)