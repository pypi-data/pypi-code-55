import platform
import sys
from pathlib import Path
from unittest import TestCase, skipUnless

from os_release import OsRelease, parser, current_release
from os_release.parser import OsReleaseParseException


class Test(TestCase):
    def test_require_newlines(self):
        with self.assertRaises(OsReleaseParseException):
            parser.parse_str('''HELLO=world FOO=bar''')

        with self.assertRaises(OsReleaseParseException):
            parser.parse_str('''HELLO="world"FOO=bar''')

        self.assertIsNotNone(parser.parse_str('''HELLO=world
                                                 FOO=bar'''))

    def test_comments(self):
        self.assertIsNotNone(parser.parse_str(
            '''HELLO=world
        
             # test
             FOO=bar'''))

    def test_dist_files(self):
        for p in Path('dist-files').glob('*-os-release'):
            with self.subTest(file=p):
                OsRelease.read(p)

    def test_is_like(self):
        o = OsRelease.from_str('''ID=centos
                                  ID_LIKE="rhel fedora"''')

        tests = [
            ('centos', True),
            ('fedora', True),
            ('rhel', True),

            ('debian', False),
            ('ubuntu', False)
        ]

        for (s, expected) in tests:
            with self.subTest(id=s):
                self.assertEqual(o.is_like(s), expected)


    def test_parse_variable(self):
        tests = [
            # valid values
            ('FOO=bar',                         {'FOO': 'bar'}),
            ('A_B=bar',                         {'A_B': 'bar'}),
            ('A12=bar',                         {'A12': 'bar'}),
            ('_AB = c',                         {'_AB': 'c'}),
            ('FOO = \t bar \t \n',              {'FOO': 'bar'}),
            ('FOO = "bar"  ',                   {'FOO': 'bar'}),
            ("FOO = 'bar'  ",                   {'FOO': 'bar'}),
            ('FOO = " bar \t "  ',              {'FOO': ' bar \t '}),
            ("FOO = ' bar \t '  ",              {'FOO': ' bar \t '}),
            ('FOO = "\\$ \\" \\\' \\\\ \\`"',   {'FOO': '$ " \' \\ `'}),


            ('A B = c',                         None),
            ('12 = c',                          None),
            ('FOO=a$b',                         None),

        ]
        for (line, expected) in tests:
            with self.subTest(line=line):
                if expected is None:
                    with self.assertRaises(OsReleaseParseException):
                        parser.parse_str(line)
                else:
                    self.assertDictEqual(parser.parse_str(line), expected)

    @skipUnless(platform.system() == 'Linux', "requires Linux")
    def test_current_release(self):
        current_release()
