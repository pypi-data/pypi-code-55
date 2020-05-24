# coding=u8
import unittest
from datetime import datetime
from KE import KE3
from KE.v3.segment import Segment


class SegmentTestCase(unittest.TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        cls._client = KE3('device2', username='admin', password='Kyligence@2020')
        cls._cube = cls._client.cubes('kylin_sales_cube')[0]
        cls._segments = cls._cube.segments()
        cls.seg0 = cls._segments.list_segments()[0]

    def test_segment_properties(self):
        print(self.seg0.name)

    def test_from_json(self):
        segments = self._segments
        print(self._cube)
        print(segments.client)
        print(segments.segment_count)

    def test_refresh(self):
        job = self.seg0.refresh()
        print(job)

    def test_drop(self):
        self.seg0.drop()





