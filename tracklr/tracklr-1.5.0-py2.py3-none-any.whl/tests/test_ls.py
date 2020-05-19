import unittest

from tracklr.main import TracklrApp
from tracklr.ls import Ls


class TestLsCommand(unittest.TestCase):

    def test_ls(self):
        app = TracklrApp()
        ls = Ls(app, None)
