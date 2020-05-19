import unittest

from tracklr.main import TracklrApp
from tracklr.group import Group


class TestPDFCommand(unittest.TestCase):
    def test_group(self):
        app = TracklrApp()
        group = Group(app, None)
