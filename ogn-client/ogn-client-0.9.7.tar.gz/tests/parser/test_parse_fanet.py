import unittest

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.aprs_comment.fanet_parser import FanetParser


class TestStringMethods(unittest.TestCase):
    def test_position_comment(self):
        message = FanetParser().parse_position("id1E1103CE -02fpm")

        self.assertEqual(message['address_type'], 2)
        self.assertEqual(message['aircraft_type'], 7)
        self.assertFalse(message['stealth'])
        self.assertEqual(message['address'], "1103CE")
        self.assertAlmostEqual(message['climb_rate'], -2 * FPM_TO_MS, 0.1)

    def test_pseudo_status_comment(self):
        message = FanetParser().parse_position("")

        self.assertIsNone(message['address_type'])
        self.assertIsNone(message['aircraft_type'])
        self.assertIsNone(message['stealth'])
        self.assertIsNone(message['address'])
        self.assertIsNone(message['climb_rate'])

    def test_status_comment(self):
        message = FanetParser().parse_status("""Name="Roman" 16.8dB -16.7kHz 1e""")

        self.assertEqual(message['user_name'], 'Roman')
        self.assertEqual(message['signal_quality'], 16.8)
        self.assertEqual(message['frequency_offset'], -16.7)
        self.assertEqual(message['error_count'], 1)

    def test_status_comment2(self):
        message = FanetParser().parse_status("""Name="Thomas Sauter" 14.3dB -12.0kHz""")

        self.assertEqual(message['user_name'], 'Thomas Sauter')
        self.assertEqual(message['signal_quality'], 14.3)
        self.assertEqual(message['frequency_offset'], -12.0)

    def test_status_comment3(self):
        message = FanetParser().parse_status("""Name="Joerg Kaiser" 14.3dB""")

        self.assertEqual(message['user_name'], 'Joerg Kaiser')
        self.assertEqual(message['signal_quality'], 14.3)


if __name__ == '__main__':
    unittest.main()
