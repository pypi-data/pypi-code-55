# -*- coding: utf-8 -*-

from unittest import TestCase
from edutermclient.edutermclient import *

class QueryTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.valid_apikey = "4c6ef653-44cf-4537-88f5-379d41575f0a"
        self.c = EdutermClient(self.valid_apikey)

    def test_empty_query(self):
        with self.assertRaises(EdutermClientError):
            self.c.setQuery("")

    def test_simple_query(self):
        self.c.setQuery("testquery")
        self.assertEqual(self.c.query,self.c.baseurl + "testquery" + "?api_key=" + self.valid_apikey)

    def test_arg_query(self):
        self.c.setQuery("testquery", {"var1": "value1"})
        self.assertEqual(self.c.query,self.c.baseurl + "testquery" + "?api_key=" + self.valid_apikey + "&var1=value1")
