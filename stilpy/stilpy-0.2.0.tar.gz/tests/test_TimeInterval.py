import unittest
from datetime import date, datetime, timedelta

from stilpy.timeinterval import TimeInterval, DATE_SEPARATORS


class TestStartProperty(unittest.TestCase):
    # Class for testing te `start` property.

    def test_date_object(self):        
        # Test that a date object returns a ValueError        
        date_ob = date(year=2019, month=12, day=19)
        with self.assertRaises(ValueError):
            TimeInterval(start=date_ob)

    def test_datetime_datetime_object(self):        
        # Test that a datetime object returns a valid datetime object
        # for the `start` attribute.        
        date_time_ob = datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        eep_date = TimeInterval(start=date_time_ob).start
        self.assertEqual(
            date_time_ob, eep_date,
            msg="datetime from datetime and property `start` are different"
        )

    def test_string_iso_date(self):        
        # Test that a string datetimeISO format objet returns a valid
        # datetime object for the `start` attribute.        
        for sep in DATE_SEPARATORS:
            date_str = '2019{s}12{s}01 17:00:59'.format(s=sep)
            formated_date = datetime.strptime(
                date_str,
                '%Y{s}%m{s}%d %H:%M:%S'.format(s=sep)
            )
            eep_date = TimeInterval(start=date_str).start
            self.assertEqual(
                formated_date, eep_date,
                msg = "string datetime and `start` property shoud be the same"
            )

    def test_little_endian_format_date(self):        
        # Test that a string datetime with little endian format is a
        # valid datetime object for the `start` attribute.

        # Little endian format is: dd-mm-yyyy        
        for sep in DATE_SEPARATORS:
            date_str = '01{s}02{s}2019 12:24:59'.format(s=sep)
            formated_date = datetime.strptime(
                date_str,
                '%d{s}%m{s}%Y %H:%M:%S'.format(s=sep)
            )
            eep_date = TimeInterval(start=date_str).start
            self.assertEqual(
                formated_date, eep_date,
                msg = "string datetime and `start` property shoud be the same"
            )

    def test_string_iso_date_non_padded_decimals(self):        
        # Test a non string date ISO format is a valid datetime object
        # for the `start` attribute.        
        for sep in DATE_SEPARATORS:
            date_str = '2019{s}2{s}1 23:00:00'.format(s=sep)
            formated_date = datetime.strptime(
                date_str,
                '%Y{s}%m{s}%d %H:%M:%S'.format(s=sep)
            )
            eep_date = TimeInterval(start=date_str).start
            self.assertEqual(
                formated_date, eep_date,
                msg = "string datetime and `start` property shoud be the same"
            )

    def test_little_endian_format_date_non_padded_decimals(self):        
        # Test a non zedro padded string little endian format is a valid
        # datetime object for the `start` attribute.

        # Little endian format is: dd-mm-yyyy        
        for sep in DATE_SEPARATORS:
            date_str = '1{s}2{s}2019 00:15:23'.format(s=sep)
            formated_date = datetime.strptime(
                date_str,
                '%d{s}%m{s}%Y %H:%M:%S'.format(s=sep)
            )
            eep_date = TimeInterval(start=date_str).start
            self.assertEqual(
                formated_date, eep_date,
                msg = "string datetime and `start` property shoud be the same"
            )

    def test_string_iso_date_error(self):        
        # Test an string ISO datetime format with an error        
        for sep in DATE_SEPARATORS:
            date_str = '209{s}12{s}01'.format(s=sep)
            with self.assertRaises(ValueError):
                TimeInterval(start=date_str)

    def test_empty_start_attr(self):        
        # Test that an empty `start` attribute creates an object with an
        # empty string start attribbute        
        self.assertEqual(
            TimeInterval().start, ''
        )

class TestStartAndEndProperty(unittest.TestCase):
    # Class for testing the `start` and `end`properties.

    def test_complete_datetime_interval(self):        
        # Test that an `start` param < than an `end` param, both
        # datetime objects creates valid values for `start and `end`
        # properties        
        start = datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        end = start + timedelta(hours=1)
        interval = TimeInterval(start=start, end=end)
        
        self.assertEqual(
            interval.start,
            start,
            msg="start var and interval.start should be equals"
        )
        self.assertEqual(
            interval.end,
            end,
            msg="end var and interval.end should be equals"
        )

    def test_end_lower_value(self):        
        # Test that an `end` param < than an `start` param, both
        # datetime objects raises a ValueError        
        start = datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        end = start + timedelta(hours=-1)
        
        with self.assertRaises(ValueError):
            TimeInterval(start=start, end=end)

    def test_empty_end_attr(self):
        # Test that an empty `end` attr creates an empty string as
        # end property
        start = '12/12/2019 12:03:52'
        interval = TimeInterval(start=start)
        self.assertEqual(
            interval.end,
            '',
            msg='end property must be an empty string'
        )

class TestDurationAndIsPerfectProperty(unittest.TestCase):
    # Class for testing the duration and is_perfect properties.    
    def setUp(self):
        # Defines the dates
        self.start_str = '12/12/2019 12:03:52'
        self.start_str_strptimed = datetime.strptime(
            self.start_str, '%d/%m/%Y %H:%M:%S'
        )
        self.strat_dt =  datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        self.end_str = '2019-12-12 13:03:52'
        self.end_str_strptimed = datetime.strptime(
            self.end_str, '%Y-%m-%d %H:%M:%S'
        )
        self.end_dt = datetime(year=2019, month=12, day=19, hour=13, minute=17, second=10)
        self.end_lw = datetime(year=2019, month=12, day=19, hour=11, minute=17, second=10)

        # Defines the durations
        self.dt_duration = self.end_dt - self.strat_dt
        self.str_duration = self.end_str_strptimed - self.start_str_strptimed
    
    def test_duration_and_is_perfect_normal_datetime(self):
        # Test the properties with normal and valid attribbutes
        
        # That means that `start` and `end` are valid datetime and that 
        # `start` < `end`.        
        interval = TimeInterval(start=self.strat_dt, end=self.end_dt)
        self.assertEqual(
            interval.duration,
            self.dt_duration,
            msg="interval.duration and self.dt_duration should be the same"
        )
        self.assertEqual(interval.is_perfect, True)
    
    def test_duration_and_is_perfect_normal_str(self):
        # Test duration and is_perfect with valid str format datetime        
        interval = TimeInterval(start=self.start_str, end=self.end_str)
        self.assertEqual(
            interval.duration,
            self.str_duration,
            msg="interval.duration and self.str_duration should have same value"
        )
        self.assertEqual(interval.is_perfect, True)
    
    def test_duration_and_isperfect_not_start(self):
        # Test duration and is_perfect prop without `start` atributte.
        # Should return a empty str and False.        
        interval = TimeInterval(end=self.end_dt)
        self.assertEqual(
            interval.duration,
            '',
            msg="interval.duration should be an empty string"
        )
        self.assertEqual(interval.is_perfect, False)

    def test_duration_and_is_perfect_not_end(self):
        # Test duration and is_perfect prop without `end` attributte.
        # Should return an empty str and False.     
        interval = TimeInterval(start=self.start_str)
        self.assertEqual(
            interval.duration,
            '',
            msg="interval.duration should be an empty string"
        )
        self.assertEqual(interval.is_perfect, False)

class TestKwargsAttr(unittest.TestCase):
    # Class for testing the kwargs params.
    def setUp(self):
        self.strat_dt =  datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        self.end_dt = datetime(year=2019, month=12, day=19, hour=13, minute=17, second=10)
        self.aditional = {
            'name': 'Peter',
            'age': 58,
            'email': 'peter@mymail.com',
            'height': 1.56
        }
        
    def test_aditional_params(self):
        # Test that aditional params are callables.
        # The must return the expected value. 
        interval = TimeInterval(
            start=self.strat_dt,
            end=self.end_dt,
            name='Tom',
            age=45,
            height=1.78,
            is_employ=True
        )
        self.assertEqual(
            interval.name,
            'Tom',
            msg="interva.name should be 'Tom'"
        )
        self.assertEqual(
            interval.age,
            45,
            msg="interva.age should be 45"
        )
        self.assertEqual(
            interval.height,
            1.78,
            msg="interva.height should be 1.78"
        )
        self.assertEqual(
            interval.is_employ,
            True,
            msg="interva.is_employ should be True"
        )

    def test_aditional_params_dict(self):
        # Test passing aditional params in a dictionary
        interval = TimeInterval(
            start=self.strat_dt,
            end=self.end_dt,
            **self.aditional
        )
        self.assertEqual(interval.name, 'Peter')
        self.assertEqual(interval.age, 58)
        self.assertEqual(interval.email, 'peter@mymail.com')
        self.assertEqual(interval.height, 1.56)

class TestLesserThan(unittest.TestCase):
    # Test the operator <
    def setUp(self):
        
        self.dt_111710 = datetime(year=2019, month=12, day=19, hour=11, minute=17, second=10)
        self.dt_121710 =  datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        self.dt_131710 = datetime(year=2019, month=12, day=19, hour=13, minute=17, second=10)
        self.dt_134710 = self.dt_131710 + timedelta(minutes=30)
        self.dt_141710 = self.dt_121710 + timedelta(hours=2)
        self.dt_151710 = self.dt_131710 + timedelta(hours=2)

        self.int_111710_121710 = TimeInterval(start=self.dt_111710, end=self.dt_121710)
        self.int_121710_131710 = TimeInterval(start=self.dt_121710, end=self.dt_131710)
        self.int_131710_141710 = TimeInterval(start=self.dt_131710, end=self.dt_141710)

        self.int_121710_151710 = TimeInterval(start=self.dt_121710, end=self.dt_151710)
        self.int_131710_141710 = TimeInterval(start=self.dt_131710, end=self.dt_141710)

        self.int_111710_empty = TimeInterval(start=self.dt_111710, end='')
        self.int_121710_empty = TimeInterval(start=self.dt_121710, end='')

        self.int_empty_111710 = TimeInterval(start='', end=self.dt_111710)
        self.int_empty_121710 = TimeInterval(start='', end=self.dt_121710)

    def test_lt_start_and_end(self):
        # Test that a lower start and end interval is < than another.
        # self.start < other.start and self.end < self.end -> self < other.
       
        self.assertTrue(self.int_121710_131710 < self.int_131710_141710)
        self.assertFalse(self.int_131710_141710 < self.int_121710_131710)

    def test_lt_star_lesser_end_greatter(self):
        # Test a lower start, but not lower end interval.
        # self.start < other.start and self.end > self.end -> self < other.
        self.assertTrue(self.int_121710_151710 < self.int_131710_141710)
        self.assertFalse(self.int_121710_151710 > self.int_131710_141710)

    def test_lt_empty_properties(self):
        # Test for lesse than with start and/or end == '' 
        # case 6
        # self < other with self.start and other.start == ''
        self.assertTrue(
            self.int_empty_111710 < self.int_empty_121710,
            msg="{} shoud be < than {}".format(
                self.int_empty_111710,
                self.int_empty_121710
            )
        )
        # case 3
        # self < other and self.end = ''
        self.assertTrue(self.int_111710_empty < self.int_121710_131710)
        self.assertFalse(self.int_111710_empty > self.int_121710_131710)

        # case 5
        # self < other and other.start = ''
        self.assertTrue(
            self.int_111710_121710 < self.int_empty_121710,
            msg="{} shoud be < than {}".format(
                self.int_121710_131710,
                self.int_empty_121710
            )
        )
        self.assertFalse(
            self.int_111710_121710 > self.int_empty_121710,
            msg="{} shoud be > than {}".format(
                self.int_111710_121710,
                self.int_empty_121710
            )
        )

        # case 12
        # self < other and (self.end and other. end) = '' True
        # self > other and (self.end and other. end) = '' False
        self.assertTrue(
            self.int_111710_empty < self.int_121710_empty,
            msg="{} shoud be < than {}".format(
                self.int_111710_empty,
                self.int_121710_empty
            )
        )
        self.assertFalse(
            self.int_111710_empty > self.int_121710_empty,
            msg="{} shoud be > than {}".format(
                self.int_111710_empty,
                self.int_121710_empty
            )
        )

        # case 1
        # self < other and self.start = '' True
        # self > other and self.start = '' False
        self.assertTrue(
            self.int_empty_111710 < self.int_121710_131710,
            msg="{} shoud be < than {}".format(
                self.int_empty_111710,
                self.int_121710_131710
            )
        )
        self.assertFalse(
            self.int_empty_111710 > self.int_121710_131710,
            msg="{} shoud be > than {}".format(
                self.int_empty_111710,
                self.int_121710_131710
            )
        )

        # case 9
        # self < other and other.end = '' True
        # self > other and other.end = '' False
        self.assertTrue(
            self.int_111710_121710 < self.int_121710_empty,
            msg="{} shoud be < than {}".format(
                self.int_empty_111710,
                self.int_empty_121710
            )
        )
        self.assertFalse(
            self.int_111710_121710 > self.int_121710_empty,
            msg="{} shoud be > than {}".format(
                self.int_empty_111710,
                self.int_empty_121710
            )
        )

        # case 10
        # self < other and (self.start and other.end) = '' True
        # self > other and (self.start and other.end) = '' False
        self.assertTrue(
            self.int_empty_111710 < self.int_121710_empty,
            msg="{} shoud be < than {}".format(
                self.int_empty_111710,
                self.int_121710_empty
            )
        )
        self.assertFalse(
            self.int_empty_111710 > self.int_121710_empty,
            msg="{} shoud be > than {}".format(
                self.int_empty_111710,
                self.int_121710_empty
            )
        )

        # case 8
        # self < other and (self.end and other.start) = '' True
        # self > other and (self.end and other.start) = '' False
        self.assertTrue(
            self.int_111710_empty < self.int_empty_121710,
            msg="{} shoud be < than {}".format(
                self.int_111710_empty,
                self.int_empty_121710
            )
        )
        self.assertFalse(
            self.int_111710_empty > self.int_empty_121710,
            msg="{} shoud be > than {}".format(
                self.int_111710_empty,
                self.int_empty_121710
            )
        )

class testEqualThan(unittest.TestCase):
    # Test the operator ==
    def setUp(self):
        
        self.dt_111710 = datetime(year=2019, month=12, day=19, hour=11, minute=17, second=10)
        self.dt_121710 =  datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        self.dt_131710 = datetime(year=2019, month=12, day=19, hour=13, minute=17, second=10)
 

        self.int_111710_121710_1 = TimeInterval(start=self.dt_111710, end=self.dt_121710)
        self.int_111710_121710_2 = TimeInterval(start=self.dt_111710, end=self.dt_121710)
       
        self.int_111710_empty_1 = TimeInterval(start=self.dt_111710, end='')
        self.int_111710_empty_2 = TimeInterval(start=self.dt_111710, end='')
        
        self.int_empty_111710_1 = TimeInterval(start='', end=self.dt_111710)
        self.int_empty_111710_2 = TimeInterval(start='', end=self.dt_111710)
        self.int_empty_121710 = TimeInterval(start='', end=self.dt_121710)
    
    def test_true_equals(self):
        # Test that two identic start and end itervals are equals
        self.assertTrue(
            self.int_111710_121710_1 == self.int_111710_121710_2,
            msg="{} and {} shoutld be equals".format(
                self.int_111710_121710_1,
                self.int_empty_111710_2
            )
        )

    def test_true_empty_str_cases(self):
        # Test empty atr start or end properties cases
        # Case 6: empty self.start and other.start
        self.assertTrue(
            self.int_empty_111710_1 == self.int_empty_111710_2,
            "Case 6\n{} and {} shoutld be equals".format(
                self.int_empty_111710_1,
                self.int_empty_111710_2
            )
        )

        # Case 12: empty self.end and other.end
        self.assertTrue(
            self.int_111710_empty_1 == self.int_111710_empty_2,
            msg="Case 12\n{} and {} shoutld be equals".format(
                self.int_111710_empty_1,
                self.int_111710_empty_2
            )
        )

        # Case 1: empty self.start
        self.assertTrue(
            self.int_empty_121710 == self.int_111710_121710_2,
            msg="Case 1\n{}\nand {}\n shout be equals".format(
                self.int_empty_121710,
                self.int_111710_121710_2
            )
        )

        # Case 3: empty self.end
        self.assertTrue(
            self.int_111710_empty_1 == self.int_111710_121710_2,
            msg="Case 3\n{}\nand {}\nshout be equals".format(
                self.int_111710_empty_1,
                self.int_111710_121710_2
            )
        )

        # Case 5: empty other.start
        self.assertTrue(
            self.int_111710_121710_2 == self.int_empty_121710,
            msg="Case 5\n{}\nand {}\nshout be equals".format(
                self.int_111710_121710_2,
                self.int_empty_121710
            )
        )

        # Case 9: empty other.end
        self.assertTrue(
            self.int_111710_121710_2 == self.int_111710_empty_1,
            msg="Case 9\n{}\nand {}\nshout be equals".format(
                self.int_111710_121710_2,
                self.int_111710_empty_1
            )
        )

        # Case 10: emtpy self.start and other.end
        self.assertTrue(
            self.int_empty_111710_2 == self.int_111710_empty_2,
            msg="Case 10:\n{}\nand {}\nshout be equals".format(
                self.int_empty_111710_2,
                self.int_111710_empty_2
            )
        )

        # Case 8: empty self.end and other.start
        self.assertTrue(
            self.int_111710_empty_1 == self.int_empty_111710_1,
            msg="Case 8\n{}\nand {}\nshout be equals".format(
                self.int_111710_empty_1,
                self.int_empty_111710_1
            )
        )

class testSortedTimeIntervals(unittest.TestCase):
    # Test that TimeElements can be sorted properly in a list
    def setUp(self):
        
        self.dt_111710 = datetime(year=2019, month=12, day=19, hour=11, minute=17, second=10)
        self.dt_121710 =  datetime(year=2019, month=12, day=19, hour=12, minute=17, second=10)
        self.dt_131710 = datetime(year=2019, month=12, day=19, hour=13, minute=17, second=10)
        self.dt_134710 = self.dt_131710 + timedelta(minutes=30)
        self.dt_141710 = self.dt_121710 + timedelta(hours=2)
        self.dt_151710 = self.dt_131710 + timedelta(hours=2)

        self.int_111710_121710 = TimeInterval(start=self.dt_111710, end=self.dt_121710)
        self.int_121710_131710 = TimeInterval(start=self.dt_121710, end=self.dt_131710)
        self.int_131710_141710 = TimeInterval(start=self.dt_131710, end=self.dt_141710)

        self.int_121710_151710 = TimeInterval(start=self.dt_121710, end=self.dt_151710)
        self.int_131710_141710 = TimeInterval(start=self.dt_131710, end=self.dt_141710)

        self.int_111710_empty = TimeInterval(start=self.dt_111710, end='')
        self.int_121710_empty = TimeInterval(start=self.dt_121710, end='')

        self.int_empty_111710 = TimeInterval(start='', end=self.dt_111710)
        self.int_empty_121710 = TimeInterval(start='', end=self.dt_121710)

        self.all = []
        self.perfect = []

        # Filling the perfect list, with only complete intervals
        for key, value in self.__dict__.items():
            if key.startswith("int_") and key.find('empty') is -1:
                self.perfect.append(value)

        # Filling the all list, with every interval
        for key, value in self.__dict__.items():
            if key.startswith("int_"):
                self.all.append(value)
    
    def test_sorting_complete_intervals(self):
        # Test that elements with no empty str parameters get sorted
        # Uncomment for visual test that the list are ordered
        # for interval in self.perfect:
        #     print(interval)
        # print("---------------------------------------")
        # for interval in sorted(self.perfect):
        #     print(interval)
        # print("---------------------------------------")
        sorted_perfect = sorted(self.perfect)
        for i, interval in enumerate(sorted_perfect):
            if i is not 0:
                self.assertLessEqual(
                    sorted_perfect[i - 1],
                    interval,
                    msg="{}\nshould be <= than\n{}".format(
                        sorted_perfect[i - 1],
                        interval
                    )
                )
    
    def test_sorting_incomplete_intervals(self):
        # Test that elements with empty str parameters get sorted
        # Uncomment for visual test that the list are ordered
        # print("---------------------------------------")
        # for interval in self.all:
        #     print(interval)
        # print("---------------------------------------")
        # for interval in sorted(self.all):
        #     print(interval)
        sorted_all = sorted(self.all)
        for i, interval in enumerate(sorted_all):
            if i is not 0:
                self.assertLessEqual(
                    sorted_all[i - 1],
                    interval
                )

                
if __name__ == '__main__':
    unittest.main()