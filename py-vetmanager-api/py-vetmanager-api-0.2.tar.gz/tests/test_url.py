import unittest
from vetmanager.url import Protocol, Url
from vetmanager.host import FakeHost


class TestUrl(unittest.TestCase):

    def test_protocol(self):
        self.assertEqual(
            str(
                Protocol('http')
            ),
            'http://'
        )

    def test_url(self):
        self.assertEqual(
            str(
                Url(
                    Protocol('http'),
                    FakeHost()
                )
            ),
            'http://fake.host'
        )


if __name__ == '__main__':
    unittest.main()
