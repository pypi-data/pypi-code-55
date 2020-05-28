import unittest
from datetime import datetime
from urllib.request import Request

from securenative.config.configuration_manager import ConfigurationManager
from securenative.event_manager import EventManager


class SampleEvent(object):

    def __init__(self):
        self.event_type = "custom-event"
        self.timestamp = datetime.now().strftime("%Y-%d-%dT%H:%M:%S.%fZ")


class EventManagerTest(unittest.TestCase):

    def setUp(self):
        self.event = SampleEvent()

    def test_send_async_event_with_status_code_200(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)
        event_manager.start_event_persist()

        event_manager.send_async(self.event, "some-path/to-api")

        try:
            expected = "{\"eventType\":\"custom-event\"}"
            req = Request  # TODO!
            self.assertEqual(expected, req.data)
        finally:
            event_manager.stop_event_persist()

    def test_should_handle_invalid_json_response_with_status_200(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)
        event_manager.start_event_persist()

        try:
            event_manager.send_async(self.event, "some-path/to-api")
            req = Request  # TODO!
            self.assertIsNotNone(req.data)
        finally:
            event_manager.stop_event_persist()

    def test_should_successfully_send_sync_event_with_status_code_200(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        res_body = "{ \"data\": true }"
        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)

        data = event_manager.send_sync(self.event, "some-path/to-api", False)
        self.assertEqual(res_body, data)

    def test_should_send_sync_event_and_handle_invalid_json_response(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)

        resp = event_manager.send_sync(self.event, "some-path/to-api", False)

        self.assertIsNone(resp)

    def test_should_send_sync_event_and_handle_invalid_request_url(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)

        self.assertIsNone(event_manager.send_sync(self.event, "path what", False))

    def test_should_send_sync_event_and_fail_when_status_code_401(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)

        self.assertIsNone(event_manager.send_sync(self.event, "some-path/to-api", False))

    def test_should_send_sync_event_and_fail_when_status_code_500(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)

        self.assertIsNone(event_manager.send_sync(self.event, "some-path/to-api", False))
