#!/usr/bin/env python

"""Tests for `w7x` package."""

import unittest


class Test_w7x(unittest.TestCase):
    """Tests for `w7x` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_version_type(self):
        """Assure that version type is str."""
        import w7x
        self.assertIsInstance(w7x.__version__, str)
