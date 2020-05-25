import json
import unittest

import requests
from uuid import uuid4

from hoss_agent import Client
from unittest.mock import MagicMock, patch

from hoss_agent.conf.constants import EVENT

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


# test httplib instrumentation by calling higher level http client method and verify that we can capture the
# call correctly
class TestHttpLibInstrumentation(unittest.TestCase):
    def setUp(self):
        self.api_id = "a2b1bb79-22a6-44e6-8ea5-067aa54a5a2c"
        self.client = Client(
            api_ids={
                "postman-echo.com": self.api_id,
            },
        )
        self.mocked_queue = MagicMock()
        self.client.instrument()
        # mock start_thread of client & transport to prevent threads from being created. We are only interested in
        # data received by _transport.queue method
        self.client.start_threads = MagicMock()
        self.client._transport.start_threads = MagicMock()
        self.client._transport.queue = self.mocked_queue

    def test_urllib(self):
        request_id = str(uuid4())
        url = "https://postman-echo.com/get?id=" + request_id
        response = urlopen(url)
        self.assertEqual(response.getcode(), 200)
        response_payload = json.loads(response.read())
        self.assertEqual(response_payload['args']['id'], request_id)
        self.mocked_queue.assert_called()
        event_type = self.mocked_queue.call_args_list[0][0][0]
        event = self.mocked_queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'GET')
        self.assertEqual(event['request']['url'], url)

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_requests(self):
        request_id = str(uuid4())
        url = "https://postman-echo.com/get?id=" + request_id
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.mocked_queue.assert_called()

        event_type = self.mocked_queue.call_args_list[0][0][0]
        event = self.mocked_queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'GET')
        self.assertEqual(event['request']['url'], url)
        self.assertEqual(event['request']['body'], '')

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(request_id, response.json()['args']['id'])
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_multiple_reads(self):
        request_id = str(uuid4())
        url = "https://postman-echo.com/get?id=" + request_id
        response = urlopen(url)
        response.read()
        response.read()

        self.mocked_queue.assert_called_once()