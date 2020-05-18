#!/usr/bin/env python

"""Tests for `tfields` package."""

import unittest


class Test_tfields(unittest.TestCase):
    """Tests for `tfields` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_version_type(self):
        """Assure that version type is str."""
        import tfields
        self.assertIsInstance(tfields.__version__, str)
