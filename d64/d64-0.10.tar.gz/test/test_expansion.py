import unittest

import d64.vic20


class TestExpansion(unittest.TestCase):

    def test_expansion(self):
        self.assertEqual(d64.vic20.expansion_required(0x1000, 0x250), (False, False, False, False, False))
        self.assertEqual(d64.vic20.expansion_required(0x401, 0x1050), (True, False, False, False, False))
        self.assertEqual(d64.vic20.expansion_required(0x1201, 0x2360), (False, True, False, False, False))
        self.assertEqual(d64.vic20.expansion_required(0x1201, 0x4360), (False, True, True, False, False))
        self.assertEqual(d64.vic20.expansion_required(0x1201, 0x6360), (False, True, True, True, False))
        self.assertEqual(d64.vic20.expansion_required(0xA000, 0x1000), (False, False, False, False, True))
