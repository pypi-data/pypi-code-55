from mock import patch, Mock
from whoishistory import Requester

import unittest
import requests
import io

_user_agent = "test-user-agent"


def mocked_requests(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, body, status_code):
            super().__init__()
            self.status_code = status_code

            self.raw = io.BytesIO(bytes(body, encoding="utf8"))

    if args[1] == 'http://test.test/200':
        return MockResponse(str(args) + str(kwargs), 200)
    elif args[1] == 'http://test.test/500':
        return MockResponse('', 500)

    return MockResponse('999', 999)


class RequesterTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('whoishistory.requester.requests.request', side_effect=mocked_requests)
    def test_url(self, mock_urlopen):
        requester = Requester(_user_agent)
        res = requester.request('http://test.test/200')
        self.assertEqual(
            res.text,
            "('GET', 'http://test.test/200')"
            "{'headers': {'Accept': 'application/json', 'User-Agent': 'test-user-agent'}, 'params': {}}",
        )

    @patch('whoishistory.requester.requests.request', side_effect=mocked_requests)
    def test_method(self, mock_urlopen):
        requester = Requester(_user_agent)
        res = requester.request('http://test.test/200', method="POST")
        self.assertEqual(
            res.text,
            "('POST', 'http://test.test/200')"
            "{'headers': {'Accept': 'application/json', 'User-Agent': 'test-user-agent'}, 'params': {}}",
        )

    @patch('whoishistory.requester.requests.request', side_effect=mocked_requests)
    def test_headers(self, mock_urlopen):
        requester = Requester(_user_agent)
        res = requester.request('http://test.test/200', method="POST",
                                headers={'My-Header': 'value', 'Accept': 'application/xml'})
        self.assertEqual(
            res.text,
            "('POST', 'http://test.test/200')"
            "{'headers': {'My-Header': 'value', 'Accept': 'application/json', 'User-Agent': 'test-user-agent'}, "
            "'params': {}}",
        )

    @patch('whoishistory.requester.requests.request', side_effect=mocked_requests)
    def test_query_params(self, mock_urlopen):
        requester = Requester(_user_agent)
        res = requester.request('http://test.test/200', method="POST",
                                params={'MyParam': 'value'})
        self.assertEqual(
            res.text,
            "('POST', 'http://test.test/200')"
            "{'headers': {'Accept': 'application/json', 'User-Agent': 'test-user-agent'}, "
            "'params': {'MyParam': 'value'}}",
        )

    def tearDown(self):
        pass
