import unittest

from tracklr import Tracklr


class TestTracklr(unittest.TestCase):
    def setUp(self):

        self.tracklr = Tracklr()

    def test_tracklr_init(self):

        self.assertIn("bdtrpfi80dtav668iqd38oqi7g", self.tracklr.__config__)

    def test_tracklr_report(self):

        report = self.tracklr.get_report(None, None, None, None, None)

    def test_tracklr_banner(self):

        banner = self.tracklr.banner(None, use_figlet=False)

        self.assertIn("Tracklr v", banner)
