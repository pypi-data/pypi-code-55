import unittest

from d64 import DOSPath


class TestWildcards(unittest.TestCase):

    def test_wildcards_plain(self):
        self.assertTrue(DOSPath.wildcard_match(b'EXACT', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXYCT', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXACTLY', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXA', 'PRG', 'EXACT'))

    def test_wildcards_single(self):
        self.assertTrue(DOSPath.wildcard_match(b'SINGLE', 'PRG', 'SINGL?'))
        self.assertTrue(DOSPath.wildcard_match(b'SINGLE', 'PRG', '?INGLE'))
        self.assertFalse(DOSPath.wildcard_match(b'SINGLE', 'PRG', 'SINGLE?'))

    def test_wildcards_multi(self):
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIPLE*'))
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIPL*'))
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIP*'))
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', '*'))

    def test_wildcards_type(self):
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=PRG'))
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=P'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=S'))

    def test_wildcards_mixed(self):
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPER', 'PRG', 'TYPE=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE=SEQ'))
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE*=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE*=SEQ'))

    def test_wildcards_bad(self):
        with self.assertRaises(ValueError):
            DOSPath.wildcard_match(b'EXACT', 'PRG', 'EXACT=')


if __name__ == '__main__':
    unittest.main()
