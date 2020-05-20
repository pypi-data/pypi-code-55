# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from decimal import Decimal

from pyrecursive import _string_types, pyrecursive


class PyRecursiveSingleAttributeTestCase(unittest.TestCase):
    def test_string(self):
        self.assertEquals(pyrecursive('abc', lambda x: x * 2), 'abcabc')

    def test_string_special_chars(self):
        self.assertEquals(pyrecursive('úá¬a平仮名, ひらがな', lambda x: x * 2), 'úá¬a平仮名, ひらがなúá¬a平仮名, ひらがな')

    def test_int(self):
        self.assertEquals(pyrecursive(21, lambda x: x * 2), 42)

    def test_float(self):
        self.assertEquals(pyrecursive(21.2, lambda x: x * 2), 42.4)

    def test_decimal(self):
        self.assertEquals(pyrecursive(Decimal('1'), lambda x: x * 2), Decimal('2'))

    def test_list(self):
        self.assertEquals(pyrecursive([1, 2, 3], lambda x: x * 2), [2, 4, 6])

    def test_tuple(self):
        self.assertEquals(pyrecursive(tuple([1, 2, 3]), lambda x: x * 2), tuple([2, 4, 6]))

    def test_set(self):
        self.assertEquals(pyrecursive(set([1, 2, 3]), lambda x: x * 2), set([2, 4, 6]))

    def test_dict(self):
        self.assertEquals(pyrecursive({'value': 1}, lambda x: x * 2), {'value': 2})
        self.assertEquals(pyrecursive({'value': 1}, lambda x: x * 2, transform_dict_keys=True), {'valuevalue': 2})
        self.assertEquals(pyrecursive({'value': 1}, lambda x: x * 2, transform_dict_values=False), {'value': 1})

    def test_custom_rules(self):
        string_type = _string_types[0]
        custom_rules = {string_type: lambda x: x}
        self.assertEquals(pyrecursive([1, 'banana'], lambda x: x * 2, custom_rules=custom_rules), [2, 'banana'])


class PyRecursiveRecursionTestCase(unittest.TestCase):
    def test_case1(self):
        data = {
            'key': [1, 2, 3, {
                'inner_key': 'inner_value',
                (10, 20): [30, 40, 50],
            }],
        }

        self.assertEquals(pyrecursive(data, lambda x: x * 2), {
            'key': [2, 4, 6, {
                'inner_key': 'inner_valueinner_value',
                (10, 20): [60, 80, 100],
            }]
        })

        self.assertEquals(pyrecursive(data, lambda x: x * 2, transform_dict_keys=True), {
            'keykey': [2, 4, 6, {
                'inner_keyinner_key': 'inner_valueinner_value',
                (20, 40): [60, 80, 100],
            }]
        })

    def test_case2(self):
        data = [
            'aa', 10, 20.0, [
                tuple([
                    Decimal('30'), {
                        'answer': set([
                            42
                        ])
                    }
                ])
            ]
        ]

        self.assertEquals(pyrecursive(data, lambda x: x * 2), [
            'aaaa', 20, 40.0, [
                tuple([
                    Decimal('60'), {
                        'answer': set([
                            84
                        ])
                    }
                ])
            ]
        ])

        self.assertEquals(pyrecursive(data, lambda x: x * 2, custom_rules={set: lambda x: None}), [
            'aaaa', 20, 40.0, [
                tuple([
                    Decimal('60'), {
                        'answer': None
                    }
                ])
            ]
        ])
