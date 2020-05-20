from __future__ import with_statement
import os
import unittest
from datetime import datetime
from KE import KE3, KE4, KE
import pandas as pd


class QueryTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE3('device2', username='admin', password='Kyligence@2020')

    def test_query1(self):
        res = self._client.query(sql='select count(1) from kylin_sales group by PART_DT;', project='learn_kylin')
        print(res.df)
