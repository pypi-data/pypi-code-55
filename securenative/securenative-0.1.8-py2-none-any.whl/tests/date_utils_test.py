import unittest
from datetime import datetime

from securenative.utils.date_utils import DateUtils


class DateUtilTest(unittest.TestCase):

    def test_to_timestamp(self):
        iso_8601_date = "2000-01-01T00:00:00.000Z"
        result = DateUtils.to_timestamp(iso_8601_date)

        self.assertEqual(datetime.strptime(iso_8601_date, "%Y-%m-%dT%H:%M:%S.%f%z"), result)

