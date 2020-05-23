from unittest import TestCase
from src.InlineClass.InlineClass import InlineClass


class TestInlineClass(TestCase):
    @staticmethod
    def _build_test_object(deep=False):
        return InlineClass({"aa": 123, "bb": "abc", "cc": {"a1": 1}}, deep=deep)

    def test_simple_create_object(self):
        obj = self._build_test_object()
        self.assertTrue(isinstance(obj, InlineClass))
        self.assertEqual(123, obj.aa)
        self.assertEqual("abc", obj.bb)
        self.assertTrue(isinstance(obj.cc, dict))

    def test_deep_create_object(self):
        obj = self._build_test_object(deep=True)
        self.assertTrue(isinstance(obj, InlineClass))
        self.assertEqual(123, obj.aa)
        self.assertEqual("abc", obj.bb)
        self.assertTrue(isinstance(obj.cc, InlineClass))
        self.assertEqual(obj.cc.a1, 1)
