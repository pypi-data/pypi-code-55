# coding=u8
import unittest
from datetime import datetime
from KE import KE
from KE.v4.segment import Segment


class SegmentsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4)
        cls.model = cls.client.models(name='kylin_sales_cube', project='learn_kylin')[0]
        cls.segments = cls.model.segments()

    def test_from_json(self):
        segments = self.segments
        print(self.model)
        print(segments.client)
        print(segments.segment_count)

    def test_merge(self):
        segments = self.segments
        print(segments.model)
        self.segments.merge(force=False)
        #self._segments.merge(force=True)

    def test_refresh(self):
        segments = self.segments
        print(segments)
        segments.refresh()

    def test_drop(self):
        model = self.client.models(name='kylin_sales_cube')[0]
        segments = model.segments()
        print(segments)
        segments.drop()

    def test_list_segments(self):
        seg_list = self.segments.list_segments()
        print(seg_list)
        print(type(seg_list[0]))
        # self.assertNotIsInstance(seg_list[0], Segment)



