"""
Internal unit-testing utilities.
"""

import unittest

from xtools import base

TEST_URL_PREFIX = "m://x"


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = base.BASE_URL
        setattr(base, "BASE_URL", TEST_URL_PREFIX)

    def tearDown(self):
        setattr(base, "BASE_URL", self.base_url)