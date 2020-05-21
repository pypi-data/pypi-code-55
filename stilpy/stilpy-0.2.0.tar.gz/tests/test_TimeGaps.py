import unittest
from datetime import datetime, timedelta
import sqlite3
from operator import itemgetter

from stilpy import TimeGaps, TimeInterval



class TestTimeGaps(unittest.TestCase):
    # Test that a list of dicts that makes a valid TimeGaps instance.
    #
    # The dict must have:
    #     * A pair of key-value element with a datetime objec or datetime
    #     formatted string
    #     * A pair of key-value element that tells if the datetime element
    #     is an start point or an exit point
    
    # List of dicts
    list_dict = [
        {
            't_dt':'start',
            'dt': '2019-12-19 10:00:00'
        },
        {
            't_dt':'end',
            'dt': '2019-12-19 13:30:20'
        },
        {
            't_dt':'start',
            'dt': '2019-12-19 14:30:00'
        },
        {
            't_dt':'start',
            'dt': '2019-12-19 15:30:00'
        },
        {
            't_dt':'end',
            'dt': '2019-12-19 17:00:35'
        },
        {
            't_dt':'start',
            'dt': '2019-12-19 09:00:00'
        }
    ]
    # List of lists (done this way for Python 3.5 not ordering dicts)
    list_ls = []
    for reg in list_dict:
        row = []
        row.append(reg['t_dt'])
        row.append(reg['dt'])
        list_ls.append(row)
    # The check list for both list of dicts an list of lists
    ls_test = (
        {
            'start': TimeInterval.str_to_datetime(list_dict[5]['dt']),
            'end': ''
        },
        {
            'start': TimeInterval.str_to_datetime(list_dict[0]['dt']),
            'end': TimeInterval.str_to_datetime(list_dict[1]['dt']),
        },
        {
            'start': TimeInterval.str_to_datetime(list_dict[2]['dt']),
            'end': ''
        },
        {
            'start': TimeInterval.str_to_datetime(list_dict[3]['dt']),
            'end': TimeInterval.str_to_datetime(list_dict[4]['dt'])
        }
    )
    
    # Creating a list of dicts with additional atrrs for groyp by
    person1 = 'Eve Palmer'
    person2 = 'Moses Farrel'
    person3 = 'Cecilia Park'

    keys_dicts = [
        {
            'name': person1.split()[0],
            'surname': person1.split()[1],
            't_dt':'start',
            'dt': '2019-12-19 10:00:00',
        },
        {
            'name': person3.split()[0],
            'surname': person3.split()[1],
            't_dt':'end',
            'dt': '2019-12-19 11:00:05'
        },
        {
            'name': person2.split()[0],
            'surname': person2.split()[1],
            't_dt':'start',
            'dt': '2019-12-19 10:00:05'
        },
        {
            'name': person1.split()[0],
            'surname': person1.split()[1],
            't_dt':'end',
            'dt': '2019-12-19 13:30:20'
        },
        {
            'name': person2.split()[0],
            'surname': person2.split()[1],
            't_dt':'end',
            'dt': '2019-12-19 13:45:15'
        },
        {
            'name': person1.split()[0],
            'surname': person1.split()[1],
            't_dt':'start',
            'dt': '2019-12-19 14:30:00'
        },
        {
            'name': person3.split()[0],
            'surname': person3.split()[1],
            't_dt':'start',
            'dt': '2019-12-19 15:30:00'
        },
        {
            'name': person3.split()[0],
            'surname': person3.split()[1],
            't_dt':'end',
            'dt': '2019-12-19 17:00:35'
        },
        {
            'name': person2.split()[0],
            'surname': person2.split()[1],
            't_dt':'start',
            'dt': '2019-12-19 09:00:00'
        }
    ]
    # List of list with additional attrs
    # (done this way for Python 3.5 not ordering dicts)
    keys_ls = []
    for reg in keys_dicts:
        row = []
        row.append(reg['name'])
        row.append(reg['surname'])
        row.append(reg['t_dt'])
        row.append(reg['dt'])
        keys_ls.append(row)


    key_dicts_perfect = []
    for i, el in enumerate(keys_dicts):
        if i not in (1, 5, 8):  # the index of the imperfect rows
            key_dicts_perfect.append(el)
    
    # The test list for additonal attrs lists
    keys_test = (
        {
            'name': keys_dicts[8]['name'],
            'surname': keys_dicts[8]['surname'],
            'start': TimeInterval.str_to_datetime(keys_dicts[8]['dt']),
            'end': ''
        },
        {
            'name': keys_dicts[0]['name'],
            'surname': keys_dicts[0]['surname'],
            'start': TimeInterval.str_to_datetime(keys_dicts[0]['dt']),
            'end': TimeInterval.str_to_datetime(keys_dicts[3]['dt'])
        },
        {
            'name': keys_dicts[2]['name'],
            'surname': keys_dicts[2]['surname'],
            'start': TimeInterval.str_to_datetime(keys_dicts[2]['dt']),
            'end': TimeInterval.str_to_datetime(keys_dicts[4]['dt'])
        },
        {
            'name': keys_dicts[1]['name'],
            'surname': keys_dicts[1]['surname'],
            'start': '',
            'end': TimeInterval.str_to_datetime(keys_dicts[1]['dt'])
        },
        {
            'name': keys_dicts[5]['name'],
            'surname': keys_dicts[5]['surname'],
            'start': TimeInterval.str_to_datetime(keys_dicts[5]['dt']),
            'end': ''
        },
        {
            'name': keys_dicts[6]['name'],
            'surname': keys_dicts[6]['surname'],
            'start': TimeInterval.str_to_datetime(keys_dicts[6]['dt']),
            'end': TimeInterval.str_to_datetime(keys_dicts[7]['dt'])
        },
    )
    # Order the key_test in groups for testing grouped_intervals attr
    keys_test_groups = (
        [keys_test[0], keys_test[2]],
        [keys_test[1], keys_test[4]],
        [keys_test[3], keys_test[5]]
    )

    @classmethod
    def setUpClass(cls):
        # Set the durations of the test lists for every intervall
        TestTimeGaps.set_duration(cls.ls_test)
        TestTimeGaps.set_duration(cls.keys_test)

        # Connect to a temp database and creates a table
        cls.con = sqlite3.connect(":memory:")
        cls.con.row_factory = sqlite3.Row
        cls.cur = cls.con.cursor()
        cls.cur.execute(
            '''
            CREATE TABLE simple_intervals (
                t_dt TEXT,
                dt DATETIME
            )
            '''
        )
        cls.cur.execute(
            '''
            CREATE TABLE attrs_intervals (
                name TEXT,
                surname TEXT,
                t_dt TEXT,
                dt DATETIME
            )
            '''
        )
        cls.cur.executemany(
            'INSERT INTO simple_intervals VALUES (?,?)',
            cls.list_ls
        )
        cls.cur.executemany(
            'INSERT INTO attrs_intervals VALUES (?,?,?,?)',
            cls.keys_ls
        )
        cls.simple_intv_q = cls.cur.execute(
            'SELECT * FROM simple_intervals'
        ).fetchall()
        cls.attrs_intv_q = cls.cur.execute(
            'SELECT * FROM attrs_intervals'
        ).fetchall()
                
    def setUp(self):
        self.iter_objects = TestTimeGaps.gen(self.keys_dicts)
    
    @staticmethod
    def set_duration(list_test: list):
        # Sets the duration property of every test interval
        for el in list_test:
            types = [type(el['start']), type(el['end'])]
            is_str = True if str in types else False
            el['duration'] = '' if is_str else el['end'] - el['start']

    def get_duration(self, interval):
        # Return the duration of the interval.
        d = timedelta()
        interval_ls = list(interval)
        for t in interval_ls:
            if t.is_perfect:
                d += t.duration
        return d
    @staticmethod
    def gen (list_dicts):
        # Creates a generator of objects
        Data = type('Data',(),{})
        for el in list_dicts:
            a = Data()
            for k, v in el.items():
                setattr(a, k, v)
            yield a

    def get_testing_groups(self, groups_interval, testing_ls):
        # Returns a copy in list format of the grouped time interval another
        # list that contais the list of dicts by groups for testing.
        
        for t in groups_interval.grouped_intervals:
            t_copy = list(t)
            gr = t_copy[0]
            group = (gr.name, gr.surname)
            same_group = lambda g: (g[0]['name'], g[0]['surname']) == group
            group_test = list(filter(same_group, testing_ls)).pop()
        return t_copy, group_test
    
    def instace_check(self, timegaps_int, test_list, attrs=None):

        timegaps_int = list(timegaps_int)
        # for el in timegaps_int:
        #     print(el)
        self.assertNotEqual(len(timegaps_int), 0)
        self.assertEqual(len(timegaps_int), len(test_list))
        for i, el in enumerate(timegaps_int):
            self.assertIsInstance(el, TimeInterval)
            print("The index is", i)
            self.assertEqual(
                el.start,
                test_list[i]['start']
            )
            self.assertEqual(
                el.end,
                test_list[i]['end']
            )
            self.assertEqual(
                el.duration,
                test_list[i]['duration']
            )
            if attrs is not None:
                for attr in attrs:
                    print(getattr(el, attr), '==', test_list[i][attr])
                    self.assertEqual(
                        getattr(el, attr),
                        test_list[i][attr]
                    )
            print("Everything ok")

    def test_minimal_instance(self):
        # Test a valid list without additional attr makes a valid instace.
        
        
        # Creates TimeGaps object with list of dicts
        main_info = ('t_dt', 'start', 'end', 'dt')
        ti = TimeGaps(self.list_dict, *main_info)
        # Creates TimeGaps object with list of lists
        ls_main_info = (0, 'start', 'end', 1)
        ti_ls = TimeGaps(self.list_ls, *ls_main_info)
        # Creates TimeGaps object with a sqlite3.Row fetchall
        ti_rows = TimeGaps(self.simple_intv_q, *main_info)
        # Create TimeGaps obj with a list of just two start register
        l_2start = [
            {'t': 'start', 'dt': '2020-01-15 17:00:00'},
            {'t': 'start', 'dt': '2020-01-15 18:00:00'}
        ]
        test_l_2start = [
            {
                'start': TimeInterval.str_to_datetime(l_2start[0]['dt']),
                'end': '',
                'duration': ''
            },
            {
                'start': TimeInterval.str_to_datetime(l_2start[1]['dt']),
                'end': '',
                'duration': ''
            }
        ]

        ti_2_start = TimeGaps(l_2start, 't', 'start', 'end', 'dt')
        
        
        # Run assertions
        self.instace_check(ti, self.ls_test)
        self.instace_check(ti_ls, self.ls_test)
        self.instace_check(ti_rows, self.ls_test)
        self.instace_check(ti_2_start, test_l_2start)
        
        print("==========1 reg TimeGaps")
        ls_dict_1_reg = [{'t_dt': 'start', 'dt': '2019-12-19 10:00:00'}]
        ls_dict_1_reg_test = (
            [{
            'start': TimeInterval.str_to_datetime('2019-12-19 10:00:00'),
            'end': '',
            'duration': ''
            }]
        )
        ti_1_reg_start = TimeGaps(ls_dict_1_reg, *main_info)
        self.instace_check(ti_1_reg_start, ls_dict_1_reg_test)
        
        print("Grouped intervals, without groups", ti.grouped_intervals)

        # Create a new ti for cheking that without group_by tag,
        # grouped_intervals returns a list with the same object (the
        # same properties, methods and intervals in the iterator) as
        # the intial TimeGaps instace.
        ti = TimeGaps(self.list_dict, *main_info)
        for t in ti.grouped_intervals:
            print(t.__dict__)
            print(ti.__dict__)
            self.assertDictEqual(t.__dict__, ti.__dict__)
            for i in t:
                print(i)
                
    def test_kwargs_instance(self):
        # Test a valid list with additional attr makes valid instance.
        
        
        # Creates list of dicts TimeGaps instance
        main_info = ('t_dt', 'start', 'end', 'dt')
        group_by = ('name', 'surname')
        group_by_1el = 'name'
        add_attr = ('name', 'surname')
        ti = TimeGaps(
            self.keys_dicts,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # This, with the commented line, is for testing that group_by
        # functionallity works perfectly without *args argument.
        ti_1g_el = TimeGaps(
            self.keys_dicts,
            *main_info,
            # *add_attr,
            group_by=group_by_1el
        )
        ti_rows = TimeGaps(
            self.attrs_intv_q,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # Creates list of lists TimeGaps instance
        ls_main_info = (2, 'start', 'end', 3)
        ls_group_by = (0, 1)
        
        ti_ls = TimeGaps(
            self.keys_ls,
            *ls_main_info,
            group_by=ls_group_by
        )
        ti_ls_gb0 = TimeGaps(
            self.keys_ls,
            *ls_main_info,
            group_by=0
        )
        # Creates TimeGaps obect with generator of objects
        ti_gen_ob = TimeGaps(
            self.iter_objects,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # Test instance
        self.instace_check(ti, self.keys_test, add_attr)
        self.instace_check(ti_1g_el, self.keys_test)
        self.instace_check(ti_ls, self.keys_test)
        self.instace_check(ti_rows, self.keys_test, add_attr)
        self.instace_check(ti_gen_ob, self.keys_test, add_attr)

        # Test group tags property
        ti_grouper_tags = [
            {'name': 'Cecilia', 'surname': 'Park'},
            {'name': 'Eve', 'surname': 'Palmer'},
            {'name': 'Moses', 'surname': 'Farrel'}
        ]
        ti_1g_el_grouper_tags = [
            {'name': 'Cecilia'},
            {'name': 'Eve'},
            {'name': 'Moses'}
        ]
        ti_ls_gb0_grouper_tags = [
            {0: 'Cecilia'},
            {0: 'Eve'},
            {0: 'Moses'}
        ]
        self.assertListEqual(ti.grouper_tags, ti_grouper_tags)
        self.assertListEqual(ti_1g_el.grouper_tags, ti_1g_el_grouper_tags)
        self.assertListEqual(ti_ls_gb0.grouper_tags, ti_ls_gb0_grouper_tags)
        self.assertListEqual(ti_rows.grouper_tags, ti_grouper_tags)
        self.assertListEqual(ti_gen_ob.grouper_tags, ti_grouper_tags)

        # Test that they the can't be mutated
        with self.assertRaises(AttributeError):
            ti.grouper_tags = 'new group'
            ti.grouped_intervals = 'new interval group'
        # int index can't be passed as aditional attributes
        with self.assertRaises(TypeError):
            ls_add_attr = (0, 1)
            ti_ls = TimeGaps(
                self.keys_ls,
            *ls_main_info,
            *ls_add_attr,
            group_by=ls_group_by
            )
        # The the grouped_intervals attribute
        print("=============== Grouped intervals")
        ti_groups = ti.grouped_intervals
        for t in ti_groups:
            t_copy, group_test = self.get_testing_groups(
                t, self.keys_test_groups
            )
            self.instace_check(t_copy, group_test, add_attr)
    
    def test_total_duration(self):
        # Test the total duration function.

        # Creates the imperfect TimeGaps iterator
        main_info = ('t_dt', 'start', 'end', 'dt')
        group_by = ('name', 'surname')
        add_attr = ('name', 'surname')
        ti = TimeGaps(
            self.keys_dicts,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # Creates the perfect TimeGaps iterator
        ti_p = TimeGaps(
            self.key_dicts_perfect,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        print(ti_p)
        # Test total_duration method for imperfect intervals collection
        self.assertEqual(ti.total_duration('unknown'), 'unknown')
        # Test total_duration method for perfect intervals colletion
        d = self.get_duration(ti_p)
        self.assertEqual(ti_p.total_duration('unknown'), d)

        # tota_duration in the perfect grouped_intervals
        ti_p_groups = ti_p.grouped_intervals
        for t in ti_p_groups:
            d = self.get_duration(t)
            self.assertEqual(t.total_duration('unknown'), d)

    def test_total_duration_anyway(self):
        # Test the total duration for perfect and/or imperfect intervals.

        # Creates the imperfect TimeGaps iterator
        main_info = ('t_dt', 'start', 'end', 'dt')
        group_by = ('name', 'surname')
        add_attr = ('name', 'surname')
        ti = TimeGaps(
            self.keys_dicts,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # Creates the perfect TimeGaps iterator
        ti_p = TimeGaps(
            self.key_dicts_perfect,
            *main_info,
            *add_attr,
            group_by=group_by
        )
        # Test total_duration method for imperfect intervals collection
        d_imperfect = self.get_duration(ti)
        self.assertEqual(ti.total_duration_anyway(), d_imperfect)
        # Test total_duration method for perfect intervals colletion
        d = self.get_duration(ti_p)
        self.assertEqual(ti_p.total_duration_anyway(), d)

        # tota_duration in the perfect grouped_intervals
        ti_p_groups = ti_p.grouped_intervals
        for t in ti_p_groups:
            d = self.get_duration(t)
            self.assertEqual(t.total_duration_anyway(), d)
        

if __name__ == '__main__':
    unittest.main()