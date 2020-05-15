#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the OpenPost project
"""

import os
import sys
import time
import unittest
from contextlib import contextmanager

import cli.openpost as test_module


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def suppress_allout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class ArgsObject():
    """
    Temporary object used for testing to mimic the args object
    returned by argparse.
    """
    date_name = False
    random_name = False
    FILENAME = None
    FILEPATH = None
    keep_file = False
    SECONDS = None
    url = None
    post_data = None


class MyTests(unittest.TestCase):

    def test_name_date(self):
        name = test_module.date_filename()
        self.assertEqual(len(name), 19)
        self.assertTrue(name.startswith(time.strftime('%Y%m%d')))
        self.assertTrue(name.endswith('.html'))

    def test_name_random(self):
        name = test_module.random_filename()
        self.assertEqual(len(name), 37)
        self.assertTrue(name.endswith('.html'))

    def test_name_01(self):
        args = ArgsObject()
        args.date_name = True
        args.random_name = False
        args.FILENAME = 'Test File Name'
        name = test_module.make_file_name(args)
        self.assertEqual(len(name), 19)
        self.assertTrue(name.startswith(time.strftime('%Y%m%d')))
        self.assertTrue(name.endswith('.html'))

    def test_name_02(self):
        args = ArgsObject()
        args.date_name = False
        args.random_name = True
        args.FILENAME = 'Test File Name'
        name = test_module.make_file_name(args)
        self.assertEqual(len(name), 37)
        self.assertTrue(name.endswith('.html'))

    def test_name_03(self):
        args = ArgsObject()
        args.date_name = False
        args.random_name = False
        args.FILENAME = 'Test File Name'
        name = test_module.make_file_name(args)
        self.assertEqual(len(name), 19)
        self.assertTrue(name.endswith('.html'))
        self.assertTrue(name.startswith('Test File Name'))

    def test_name_04(self):
        args = ArgsObject()
        args.date_name = False
        args.random_name = False
        name = test_module.make_file_name(args)
        self.assertEqual(name, test_module.DEFAULT_HTML_FILE)
        self.assertTrue(name.endswith('.html'))

    def test_make_file_path_01(self):
        args = ArgsObject()
        name = test_module.make_file_path(args)
        self.assertEqual(name, '.')

    def test_make_file_path_02(self):
        args = ArgsObject()
        args.FILEPATH = 'test_FILE_path'
        name = test_module.make_file_path(args)
        self.assertEqual(name, 'test_FILE_path')

    def test_make_file_path_03(self):
        args = ArgsObject()
        args.FILEPATH = 'test'
        name = test_module.make_file_path(args)
        self.assertEqual(name, 'test')

    def test_post_data_single(self):
        data = test_module.make_form_data_string(['abc=123'])
        self.assertTrue('<input type="hidden" name="abc" value="123">' in data)

    def test_post_data_multiple(self):
        data = test_module.make_form_data_string(['abc=123', 'xyz=456'])
        self.assertTrue('<input type="hidden" name="abc" value="123">' in data)
        self.assertTrue('<input type="hidden" name="xyz" value="456">' in data)

    def test_post_data_case(self):
        data = test_module.make_form_data_string(['abc=123'])
        self.assertTrue('<input type="hidden" name="ABC" value="123">' not in data)

    def test_test_url_01(self):
        data = test_module.test_url(1)
        self.assertEqual(data, 103)

    def test_test_url_02(self):
        data = test_module.test_url('')
        self.assertEqual(data, 101)

    def test_test_url_03(self):
        data = test_module.test_url(' ')
        self.assertEqual(data, 101)

    def test_test_url_04(self):
        data = test_module.test_url('embedded space')
        self.assertEqual(data, 102)

    def test_test_url_05(self):
        data = test_module.test_url('localhost')
        self.assertEqual(data, 0)

    def test_test_url_06(self):
        data = test_module.test_url('192.168.1.1')
        self.assertEqual(data, 0)

    def test_test_url_07(self):
        data = test_module.test_url('www.somewhere.com')
        self.assertEqual(data, 0)

    def test_test_url_08(self):
        data = test_module.test_url('http://www.somewhere.com')
        self.assertEqual(data, 0)

    def test_test_url_09(self):
        data = test_module.test_url('https://www.somewhere.com')
        self.assertEqual(data, 0)

    def test_test_url_10(self):
        data = test_module.test_url('www.somewhere.com/')
        self.assertEqual(data, 0)

    def test_test_url_11(self):
        data = test_module.test_url('www.somewhere.com/subdir')
        self.assertEqual(data, 0)

    def test_test_url_12(self):
        data = test_module.test_url('www.somewhere.com/subdir/')
        self.assertEqual(data, 0)

    def test_test_ttl_01(self):
        args = ArgsObject()
        args.SECONDS = None
        data = test_module.make_time_to_live(args)
        self.assertEqual(data, test_module.DEFAULT_TIME_TO_LIVE)

    def test_test_ttl_02(self):
        args = ArgsObject()
        args.SECONDS = 10
        data = test_module.make_time_to_live(args)
        self.assertEqual(data, 10)

    def test_test_ttl_03(self):
        args = ArgsObject()
        args.SECONDS = 13.5
        data = test_module.make_time_to_live(args)
        self.assertEqual(data, 13.5)

    def test_exit_missing(self):
        args = ArgsObject()
        args.url = ''
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.exit_with_error()
        self.assertEqual(err.exception.code, -1)
        # unittest.main(exit=False)

    def test_exit_unknown(self):
        args = ArgsObject()
        args.url = ''
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.exit_with_error(-1)
        self.assertEqual(err.exception.code, -1)
        # unittest.main(exit=False)

    def test_exit_101(self):
        args = ArgsObject()
        args.url = ''
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.exit_with_error(101)
        self.assertEqual(err.exception.code, 101)
        # unittest.main(exit=False)

    def test_ttl_104_1(self):
        args = ArgsObject()
        args.SECONDS = -1
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_time_to_live(args)
        self.assertEqual(err.exception.code, 104)
        # unittest.main(exit=False)

    def test_ttl_104_2(self):
        args = ArgsObject()
        args.SECONDS = 61
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_time_to_live(args)
        self.assertEqual(err.exception.code, 104)
        # unittest.main(exit=False)

    def test_path_105_1(self):
        args = ArgsObject()
        args.FILEPATH = ''
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_file_path(args)
        self.assertEqual(err.exception.code, 105)
        # unittest.main(exit=False)

    def test_path_105_2(self):
        args = ArgsObject()
        args.FILEPATH = ' '
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_file_path(args)
        self.assertEqual(err.exception.code, 105)
        # unittest.main(exit=False)

    def test_path_106(self):
        args = ArgsObject()
        args.FILEPATH = 'cli/openpost.py'
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_file_path(args)
        self.assertEqual(err.exception.code, 106)
        # unittest.main(exit=False)

    def test_name_107_1(self):
        args = ArgsObject()
        args.FILENAME = ''
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_file_name(args)
        self.assertEqual(err.exception.code, 107)
        # unittest.main(exit=False)

    def test_name_107_2(self):
        args = ArgsObject()
        args.FILENAME = ' '
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_file_name(args)
        self.assertEqual(err.exception.code, 107)
        # unittest.main(exit=False)

    def test_data_108_1(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string('')
        self.assertEqual(err.exception.code, 108)
        # unittest.main(exit=False)

    def test_data_108_2(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string(0)
        self.assertEqual(err.exception.code, 108)
        # unittest.main(exit=False)

    def test_data_108_3(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string(1.5)
        self.assertEqual(err.exception.code, 108)
        # unittest.main(exit=False)

    def test_data_108_4(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string(('a', 'b'))
        self.assertEqual(err.exception.code, 108)
        # unittest.main(exit=False)

    def test_data_108_5(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string({'key': 'value'})
        self.assertEqual(err.exception.code, 108)
        # unittest.main(exit=False)

    def test_data_109(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string(['no equals sign'])
        self.assertEqual(err.exception.code, 109)
        # unittest.main(exit=False)

    def test_data_110(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string(['=no key'])
        self.assertEqual(err.exception.code, 110)
        # unittest.main(exit=False)

    def test_data_111(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.make_form_data_string([])
        self.assertEqual(err.exception.code, 111)
        # unittest.main(exit=False)

    def test_main_0_1(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.parse_command_arguments(['--help'])
        self.assertEqual(err.exception.code, 0)
        # unittest.main(exit=False)

    def test_main_0_2(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_stdout():
                test_module.parse_command_arguments(['-h'])
        self.assertEqual(err.exception.code, 0)
        # unittest.main(exit=False)

    def test_main_2_1(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_allout():
                test_module.parse_command_arguments([])
        self.assertEqual(err.exception.code, 2)
        # unittest.main(exit=False)

    # Test disabled because missing key=value pairs no longer caught in parse_command_arguments module.

    # def test_main_2_2(self):
    #     with self.assertRaises(SystemExit) as err:
    #         with suppress_allout():
    #             test_module.parse_command_arguments(['localhost'])
    #     self.assertEqual(err.exception.code, 2)
    #     # unittest.main(exit=False)

    def test_main_2_3(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_allout():
                test_module.parse_command_arguments(['localhost', 'key=value', '-r', '-d'])
        self.assertEqual(err.exception.code, 2)
        # unittest.main(exit=False)

    def test_main_2_4(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_allout():
                test_module.parse_command_arguments(['localhost', 'key=value', '-r', '-f', 'filename'])
        self.assertEqual(err.exception.code, 2)
        # unittest.main(exit=False)

    def test_main_2_5(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_allout():
                test_module.parse_command_arguments(['localhost', 'key=value', '-d', '-f', 'filename'])
        self.assertEqual(err.exception.code, 2)
        # unittest.main(exit=False)

    def test_main_2_6(self):
        with self.assertRaises(SystemExit) as err:
            with suppress_allout():
                test_module.parse_command_arguments(['localhost', 'key=value', '-k', '-t', '5'])
        self.assertEqual(err.exception.code, 2)
        # unittest.main(exit=False)
