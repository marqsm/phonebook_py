import unittest
import os
import phonebook

phonebook = phonebook.Phonebook()


class TestPhonebook(unittest.TestCase):
    fx_pb = {}
    fx_filename = 'phonebook_fixtures.pb'

    def setUp(self):
        self.fx_pb = phonebook.pb_load(self.fx_filename)

    def test_pb_load(self):
        pb = phonebook.pb_load(self.fx_filename)
        self.assertEqual(pb, {'Sarah Orange': '1234567890',
                         'Sarah Apple': '5091234567',
                         'Jane Doe': '987654321'}
                         )

    def test_pb_parse_input_row(self):
        actual = phonebook.pb_parse_input_row('jaska 123456')
        self.assertEqual(actual, ('jaska', '123456'))

    def test_pb_parse_output_row(self):
        actual = phonebook.pb_parse_output_row('jaska jokunen', '123 456')
        self.assertEqual(actual, 'jaska jokunen 123 456\n')

    def test_pb_create(self):
        filename = '_phonebook_create_test_xxxxx.pb'
        phonebook.pb_create(filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)
        self.assertFalse(os.path.isfile(filename))


if __name__ == '__main__':
    unittest.main(exit=False)
