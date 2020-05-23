# -*- coding: utf-8 -*-

from unittest import TestCase
from edutermclient.edutermclient import *

class InitTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.valid_apikey = "4c6ef653-44cf-4537-88f5-379d41575f0a"

    def test_invalid_apikey(self):
        with self.assertRaises(EdutermClientError):
            c = EdutermClient("invalidkey")

    def test_valid_apikey(self):
        c = EdutermClient(self.valid_apikey)
        self.assertIsInstance(c,EdutermClient)

    def test_empty_endpoint(self):
        c = EdutermClient(self.valid_apikey)
        c.setEndpoint("")
        self.assertEqual(c.endpoint,"")

    def test_valid_endpoint(self):
        c = EdutermClient(self.valid_apikey)
        c.setEndpoint("test")
        self.assertEqual(c.endpoint,"&endpoint=test")
