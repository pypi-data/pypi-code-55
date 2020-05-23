from unittest import TestCase

from Version.Version import Version
from Version.VersionException import VersionException


class TestVersion(TestCase):
    def test_case1(self):
        obj1 = Version("1.2.3.4")
        obj2 = Version((1, 2, 3, 4))
        self.assertEqual((1, 2, 3, 4), obj1.get_version())
        self.assertEqual(obj1, obj2)

    def test_case2(self):
        with self.assertRaises(VersionException):
            obj1 = Version("1.2.5.4.3")

        with self.assertRaises(VersionException):
            obj1 = Version("1.2.dd")

    def test_case3(self):
        self.assertEqual(Version("1"), Version("1 "))
        self.assertEqual(Version("1.2.3.4"), Version("1.2.3.4 "))
        self.assertNotEqual(Version("1.2.3.4"), Version("1.2.3.5"))
        self.assertEqual(Version("1.2"), Version("1.2.0.0"))
        self.assertEqual(Version("1.0.0.0"), Version("1"))
        self.assertNotEqual(Version("1.2.3.4"), Version("1.2.3"))

    def test_case4(self):
        self.assertEqual((1, 2, 0, 0), Version("1.2").get_version(4))
        self.assertEqual((1, 2), Version("1.2").get_version())

    def test_case4(self):
        self.assertTrue(Version("1.2.3.4").compare(Version("1.2.3.4"), length=4))
        self.assertTrue(Version("1.2.3.4").compare(Version("1.2.3.4"), length=2))
        self.assertTrue(Version("1.2").compare(Version("1.2.3.4"), length=2))
        self.assertTrue(Version("1.2.3.4").compare(Version("1.2"), length=2))
        self.assertTrue(Version("1.2.8.8").compare(Version("1.2.1.1"), length=2))


