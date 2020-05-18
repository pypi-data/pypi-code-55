#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the proxy main method."""
from unittest import TestCase
from pacifica.proxy.__main__ import main


class TestMain(TestCase):
    """Test some of the arguments to main."""

    def test_main_stop(self):
        """Test main with stop arguments."""
        self.assertEqual(main(['--stop-after-a-moment']), 0)
