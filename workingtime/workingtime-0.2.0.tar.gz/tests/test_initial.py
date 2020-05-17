import unittest

import numpy as np
from datetime import timedelta, datetime
from workingtime.workingtime import _dates_between_dates
from workingtime import WorkingTime, Time


class InitialTest(unittest.TestCase):

    def test_dates_between_dates(self):
        now = datetime.now()
        day = timedelta(1)

        np.testing.assert_array_equal(
            _dates_between_dates(now, now), [])
        np.testing.assert_array_equal(
            _dates_between_dates(now, now + day), [])
        np.testing.assert_array_equal(
            _dates_between_dates(now, now + 2 * day),
            [now + day])

    def test_another_test(self):
        wt = WorkingTime()
        np.testing.assert_equal(
            wt.working_time(datetime(2020, 10, 3, 1),
                           datetime(2020, 10, 4, 23),
                           (Time(22, 0), Time(0, 30))).total_seconds(),
            (2.5 + 1) * 3600)


if __name__ == '__main__':
    print()
    unittest.main()
