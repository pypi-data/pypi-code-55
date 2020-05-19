from whatthefuzz.wtfuzz_core import wtfuzz
import unittest
from io import StringIO
import sys


class wtfuzzTest(unittest.TestCase):

    def test_sendSimpleRequest(self):
        url = 'http://www.example.org/'
        file = 'test/test.txt'
        w = wtfuzz()
        w.config(url, file)
        w.sendSimpleRequest()
        self.assertEqual(w.responses[url], 200, " Error sending simple request")

    def test_sendSimpleVerbRequestOK(self):
        url = 'http://www.example.org/'
        file = 'test/test.txt'
        w = wtfuzz()
        w.config(url, file)
        w.sendVerbRequest("HEAD")
        self.assertEqual(w.responses[url], 200, " Error sending simple request")

    def test_sendSimpleVerbRequestKO(self):
        url = 'http://www.example.org/'
        file = 'test/test.txt'
        w = wtfuzz()
        w.config(url, file)
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        w.sendVerbRequest("FAKE")
        output = out.getvalue().strip()
        sys.stdout = saved_stdout
        self.assertEqual(output, "Error - Verb FAKE not valid", " Error message - verb not validated")

    def test_sendFullRequest(self):
        url = 'http://www.example.org/'
        file = 'test/test.txt'
        w = wtfuzz()
        w.config(url, file)
        fullResp = {"Code": 200, "Verb": "head", "Length": 0}
        w.sendFullRequest("HEAD")
        self.assertEqual(w.fullResponses[url], fullResp, " Error sending full request")

    def test_sendAllVerbsRequest(self):
        url = 'http://www.example.org/'
        w = wtfuzz()
        w.config(url=url)
        w.sendAllVerbsRequest()
        self.assertEqual(len(w.verbResponses), 7, " Error sending all verbs request")


if __name__ == "__main__":
    unittest.main()
