# -*- coding: utf-8 -*-

from unittest import TestCase
from edutermclient.edutermclient import *
import json
from sys import version_info

class TableTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.c = EdutermClient("4c6ef653-44cf-4537-88f5-379d41575f0a")
        with open("test/example.json", "r") as f:
            self.c.response_json = json.loads(f.read())
        self.c.setTable()

    def test_table_general(self):
        self.assertEqual(len(self.c.response_table),2)
        self.assertEqual(len(self.c.response_table[0]),4)
        self.assertEqual(self.c.response_table[0]["vakLabel"],"Aardrijkskunde")
        self.assertFalse(self.c.response_table[1]["hasChildren"])

    def test_table_types(self):
        self.assertIsInstance(self.c.response_table[0]["hasChildren"],bool)
        self.assertIsInstance(self.c.response_table[0]["childCount"],int)

        if version_info.major > 2:
            self.assertIsInstance(self.c.response_table[0]["vakLabel"],str)
        else:
            self.assertIsInstance(self.c.response_table[0]["vakLabel"],unicode)
