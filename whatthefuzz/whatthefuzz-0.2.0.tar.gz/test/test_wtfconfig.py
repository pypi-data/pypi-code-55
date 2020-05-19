from whatthefuzz.wtfuzz_core import wtfconfig
import unittest
from io import StringIO
import sys


class wtfuzzTest(unittest.TestCase):

    def test_Init_OK(self):
        w = wtfconfig()
        w.setUrl('http://example.org/')
        w.getPayloads('test/actuatortest.txt')
        self.assertEqual(w.url, 'http://example.org/', 'wrong url')

    def test_urlOK2(self):
        w = wtfconfig()
        w.setUrl('http://example.org')
        w.getPayloads('test/actuatortest.txt')
        self.assertEqual(w.url, 'http://example.org/', 'wrong url')

    def test_urlKO(self):
        w = wtfconfig()
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        w.setUrl('htt://example.org/')
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        self.assertEqual(output, "url not valid", " Error message - url not valid")
        self.assertEqual(w.url, None, 'wrong url')

    def test_initPayloadOK(self):
        lines = ['', 'line1', 'line2']
        w = wtfconfig()
        w.getPayloads('test/test.txt')
        self.assertEqual(w.payloads, lines, 'file not correctly read')

    def test_readFileNotExist(self):
        w = wtfconfig()
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        w.getPayloads('noname.txt')
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        self.assertEqual(w.payloads, [], ' Payloads not initialised - File does not exist')
        self.assertEqual(output, "File not found", " Error message - file not found")

    def test_validUrlOK(self):
        w = wtfconfig()
        w.setUrl('http://example.org')
        w.getPayloads('test/test.txt')

        self.assertEqual(w.validConfig(), True, 'Validation failed - OK Test')

    def test_validUrlKO(self):
        w = wtfconfig()
        w.setUrl('www.example.org')
        w.getPayloads('test/test.txt')

        self.assertEqual(w.validConfig(), False, 'Url  validation failed - KO Test')

    def test_validPayloadsKO(self):
        w = wtfconfig()
        w.setUrl('http://example.org')
        w.getPayloads('test/tet.txt')
        self.assertEqual(w.validConfig(), False, 'Payload  validation failed - KO Test')


if __name__ == "__main__":
    unittest.main()
