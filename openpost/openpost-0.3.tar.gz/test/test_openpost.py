#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the OpenPost project
"""

import os
import sys
import unittest
from contextlib import contextmanager

import openpost as test_module


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


class MyTests(unittest.TestCase):

    def test_initialize_01(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster.url, None)
        self.assertEqual(poster.file_name, 'OpenPost.html')
        self.assertFalse(poster.keep_file)
        self.assertEqual(poster.time_to_live, 5)
        self.assertEqual(poster.form_data, {})
        self.assertEqual(poster.version(), test_module.__version__)

    def test_initialize_02(self):
        poster = test_module.OpenPost('test_url', 'test_file_name', True, 10.5, {'one': 'This is the number one.'})
        self.assertEqual(poster.url, 'test_url')
        self.assertEqual(poster.file_name, 'test_file_name.html')
        self.assertTrue(poster.keep_file)
        self.assertEqual(poster.time_to_live, 10.5)
        self.assertEqual(len(poster.form_data.keys()), 1)
        self.assertEqual(list(poster.form_data.keys()), ['one'])

    def test_edit_properties(self):
        poster = test_module.OpenPost()
        poster.url = 'test_url'
        self.assertEqual(poster.url, 'test_url')
        poster.file_name = 'test_file_name'
        self.assertEqual(poster.file_name, 'test_file_name')
        poster.keep_file = True
        self.assertTrue(poster.keep_file)
        poster.time_to_live = 10.5
        self.assertEqual(poster.time_to_live, 10.5)
        poster.form_data = {'one': 'This is the number one.'}
        self.assertEqual(len(poster.form_data.keys()), 1)
        self.assertEqual(list(poster.form_data.keys()), ['one'])

    def test_keys(self):
        poster = test_module.OpenPost()
        poster.add_key('one', 'This is the number one.')
        self.assertEqual(len(poster.form_data.keys()), 1)
        self.assertEqual(list(poster.form_data.keys()), ['one'])
        poster.clear_data()
        self.assertEqual(poster.form_data, {})
        poster.add_key('one', 'This is the number one.')
        self.assertEqual(len(poster.form_data.keys()), 1)
        self.assertEqual(list(poster.form_data.keys()), ['one'])
        poster.add_key('two', 'This is the number two.')
        self.assertEqual(len(poster.form_data.keys()), 2)
        poster.delete_key('one')
        self.assertEqual(len(poster.form_data.keys()), 1)
        self.assertEqual(list(poster.form_data.keys()), ['two'])

    def test_validate_ttl(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster._validate_ttl(0), 0)
        self.assertEqual(poster._validate_ttl('15'), 15)
        self.assertEqual(poster._validate_ttl(15.000), 15)
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_ttl('')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_ttl('zero')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_ttl(-1)
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_ttl(61)

    def test_validate_data(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster._validate_data(None), {})
        self.assertEqual(poster._validate_data({}), {})
        self.assertEqual(poster._validate_data([]), {})
        self.assertEqual(poster._validate_data(''), {})
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_data('string')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_data(['list'])
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_data(('a', 'b'))
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_data(1)
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_data(1.5)

    def test_validate_url(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster._validate_url('localhost'), 'localhost')
        self.assertEqual(poster._validate_url('https://some.test.url'), 'https://some.test.url')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url(None)
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url('')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url(' ')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url('contains space')
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url({'one': 1})
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url(['one'])
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url(1)
        with self.assertRaises(ValueError):
            with suppress_allout():
                poster._validate_url(1.5)

    def test_make_filename(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster._make_filename(None), 'OpenPost.html')
        self.assertEqual(poster._make_filename(''), 'OpenPost.html')
        self.assertEqual(poster._make_filename(' '), 'OpenPost.html')
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_filename(-1)
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_filename(10.50)
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_filename({'a': 'b'})
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_filename(['a', 'b'])
        self.assertEqual(poster._make_filename('fred.html'), 'fred.html')
        self.assertEqual(poster._make_filename(' fred.html'), 'fred.html')
        self.assertEqual(poster._make_filename('fred.html '), 'fred.html')
        self.assertEqual(poster._make_filename('fred.htm'), 'fred.htm.html')

    def test_make_string(self):
        poster = test_module.OpenPost()
        self.assertEqual(poster._make_string(None), '')
        self.assertEqual(poster._make_string(''), '')
        self.assertEqual(poster._make_string(' '), '')
        self.assertEqual(poster._make_string(' a '), 'a')
        self.assertEqual(poster._make_string(['', '', '']), '')
        self.assertEqual(poster._make_string(['', ' ', '']), '')
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_string({'a': 'b'})
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_string(10)
        with self.assertRaises(AttributeError):
            with suppress_allout():
                poster._make_string(10.5)
        with self.assertRaises(TypeError):
            with suppress_allout():
                poster._make_string(['', None, ''])
        with self.assertRaises(TypeError):
            with suppress_allout():
                poster._make_string(['', {'a': 'b'}, ''])
        with self.assertRaises(TypeError):
            with suppress_allout():
                poster._make_string(['', 10, ''])
        with self.assertRaises(TypeError):
            with suppress_allout():
                poster._make_string(['', 10.5, ''])
        with self.assertRaises(TypeError):
            with suppress_allout():
                poster._make_string(['', ['a', 'b'], ''])
