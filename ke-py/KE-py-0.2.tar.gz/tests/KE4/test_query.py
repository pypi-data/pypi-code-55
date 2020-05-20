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
        self._client = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4)

    def test_query1(self):
        query = self._client.query(sql='select PART_DT, count(1) from kylin_sales group by PART_DT;', project='learn_kylin')
        print(query.df)
        self.assertIsInstance(query.df, pd.DataFrame)
