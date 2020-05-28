import unittest

from securenative.config.configuration_manager import ConfigurationManager


class SecureNativeHttpClientTest(unittest.TestCase):

    def test_should_make_simple_post_call(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        payload = "{\"event\":\"SOME_EVENT_NAME\"}"

        res = client.post("track", payload)

        self.assertEqual(res.is_ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, "SOME_BODY")
