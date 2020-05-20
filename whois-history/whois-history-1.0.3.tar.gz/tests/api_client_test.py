import io

from whoishistory.requester import Requester
from whoishistory import ApiClient
from whoishistory.models.historic import *
from whoishistory.exceptions import EmptyResponseException, UnparsableResponseException
import unittest
import requests


class MockResponse(requests.Response):
    def __init__(self, body, status_code):
        super().__init__()
        self.status_code = status_code

        self.raw = io.BytesIO(bytes(body, encoding="utf8"))


class MockRequester(Requester):
    def __init__(self, data):
        super().__init__('test-agent')
        self.data = data

    def request(self, url, method: str = "GET", headers: dict = None, params: dict = None) -> requests.Response:
        if self.data is Exception:
            raise self.data

        resp = MockResponse(self.data, 200)

        return resp


class ApiClientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass

    def test_request(self):
        payload = '{"records":[{"domainName":"domain.test"}], "recordsCount":1}'
        fake_requester = MockRequester(payload)

        client = ApiClient('test')
        client.set_requester(fake_requester)

        res = client.purchase("domain.test")

        valid = [WhoisRecord({"domainName": "domain.test"})]

        self.assertEqual(valid, res)

    def test_error_request(self):
        payload = '{"code":999, "messages":"test error message"}'
        fake_requester = MockRequester(payload)

        client = ApiClient('test')
        client.set_requester(fake_requester)

        with self.assertRaises(ErrorMessage):
            client.purchase("domain.test")

        try:
            client.purchase("domain.test")
        except ErrorMessage as e:
            self.assertEqual('[999] test error message', e.__str__())

    def test_get_empty_response(self):
        fake_requester = MockRequester('')

        client = ApiClient('test')
        client.set_requester(fake_requester)

        with self.assertRaises(EmptyResponseException):
            client.purchase("domain.test")

    def test_get_unparsable_response(self):
        fake_requester = MockRequester('not a json')

        client = ApiClient('test')
        client.set_requester(fake_requester)

        with self.assertRaises(UnparsableResponseException):
            client.purchase("domain.test")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
