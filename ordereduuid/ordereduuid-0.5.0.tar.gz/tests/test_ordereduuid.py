import random
import unittest
import uuid

import ordereduuid

_CLOCK_SEQ_BITS = 16

class TestUUIDCreation(unittest.TestCase):
    """Test OrderedUUIDs by comparing with standard library UUIDs."""
    def test_polymorphism(self):
        u = ordereduuid.OrderedUUID()
        self._test_ordered_uuid(u)

    def test_default_constructor(self):
        u = ordereduuid.OrderedUUID()
        self._test_ordered_uuid(u)

    def test_clock_seq_constructor(self):
        n = random.getrandbits(_CLOCK_SEQ_BITS)
        u = ordereduuid.OrderedUUID(clock_seq=n)
        self._test_ordered_uuid(u)

    def test_nonrandom_node(self):
        u = ordereduuid.OrderedUUID(random_node=False)
        self._test_ordered_uuid(u)
        

    def _test_ordered_uuid(self, ordered_uuid):
        equivalent_standard_uuid = uuid.UUID(int=ordered_uuid.int)
        self.assertEqual(ordered_uuid, equivalent_standard_uuid)

