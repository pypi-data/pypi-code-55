#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `soap` package."""


import unittest

from soapcw import soapcw as soap
import numpy as np

class TestSoap(unittest.TestCase):
    """Tests for `soap` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_basic_single(self):
        """Test something."""

        arr = np.random.rand(40,40)

        sp = soap.single_detector([0,1,0],arr)

        
