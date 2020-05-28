import unittest

from securenative.api_manager import ApiManager
from securenative.config.configuration_manager import ConfigurationManager
from securenative.context.context_builder import ContextBuilder
from securenative.enums.event_types import EventTypes
from securenative.enums.risk_level import RiskLevel
from securenative.event_manager import EventManager
from securenative.event_options_builder import EventOptionsBuilder
from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException
from securenative.models.user_traits import UserTraits
from securenative.models.verify_result import VerifyResult
from securenative.utils.date_utils import DateUtils


class ApiManagerTest(unittest.TestCase):

    def setUp(self):
        self.context = ContextBuilder(). \
            with_ip("127.0.0.1"). \
            with_client_token("SECURED_CLIENT_TOKEN"). \
            with_headers(
            {
                "user-agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
            }).build()

        self.event_options = EventOptionsBuilder(EventTypes.LOG_IN). \
            with_user_id("USER_ID"). \
            with_user_traits(UserTraits("USER_NAME", "USER_EMAIL")). \
            with_context(self.context). \
            with_properties({"prop1": "CUSTOM_PARAM_VALUE",
                             "prop2": True,
                             "prop3": 3}).with_timestamp(DateUtils.to_timestamp(None)).build()

    def test_track_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(options, client)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            res = api_manager.track(self.event_options)
            expected = "{\"eventType\":\"sn.user.login\",\"userId\":\"USER_ID\",\"userTraits\":{" \
                       "\"name\":\"USER_NAME\",\"email\":\"USER_EMAIL\",\"createdAt\":null},\"request\":{" \
                       "\"cid\":null,\"vid\":null,\"fp\":null,\"ip\":\"127.0.0.1\",\"remoteIp\":null,\"headers\":{" \
                       "\"user-agent\":\"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) " \
                       "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405\"},\"url\":null,\"method\":null}," \
                       "\"properties\":{\"prop2\":true,\"prop1\":\"CUSTOM_PARAM_VALUE\",\"prop3\":3}} "

            self.assertEqual(res.body, expected)
        finally:
            event_manager.stop_event_persist()

    def test_securenative_invalid_options_exception(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        properties = {}
        for i in range(1, 12):
            properties[i] = i

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(client, options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            api_manager.track(EventOptionsBuilder(
                EventTypes.LOG_IN).with_properties(properties).build())
            self.assertRaises(SecureNativeInvalidOptionsException)
        finally:
            event_manager.stop_event_persist()

    def test_automatic_persistent_disable(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(client, options)
        api_manager = ApiManager(event_manager, options)

        self.assertIsNotNone(api_manager.track(self.event_options))

    def test_unauthorized_track_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10)

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(client, options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            self.assertIsNotNone(api_manager.track(self.event_options))
        finally:
            event_manager.stop_event_persist()

    def test_verify_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        verify_result = VerifyResult(RiskLevel.LOW, 0, {})

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(client, options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        result, body = api_manager.verify(self.event_options)

        self.assertEqual(result.risk_level, verify_result.risk_level)
        self.assertEqual(result.score, verify_result.score)
        self.assertEqual(result.triggers, verify_result.triggers)

        expected = "{\"eventType\":\"sn.user.login\",\"userId\":\"USER_ID\",\"userTraits\":{\"name\":\"USER_NAME\",\"email\":\"USER_EMAIL\",\"createdAt\":null},\"request\":{\"cid\":null,\"vid\":null,\"fp\":null,\"ip\":\"127.0.0.1\",\"remoteIp\":null,\"headers\":{\"user-agent\":\"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405\"},\"url\":null,\"method\":null},\"properties\":{\"prop2\":true,\"prop1\":\"CUSTOM_PARAM_VALUE\",\"prop3\":3}}";
        self.assertEqual(body, expected)

    def test_unauthorized_verify_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY")

        client = MockHttpClient()  # TODO!
        event_manager = EventManager(client, options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        result, body = api_manager.verify(self.event_options)

        self.assertIsNotNone(result)
        self.assertEqual(result.risk_level, RiskLevel.LOW)
        self.assertEqual(result.score, 0)
        self.assertEqual(result.triggers, 0)

        expected = "{\"eventType\":\"sn.user.login\",\"userId\":\"USER_ID\",\"userTraits\":{\"name\":\"USER_NAME'\",\"email\":\"USER_EMAIL'\",\"createdAt\":null},\"request\":{\"cid\":null,\"vid\":null,\"fp\":null,\"ip\":\"127.0.0.1\",\"remoteIp\":null,\"headers\":{\"user-agent\":\"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405\"},\"url\":null,\"method\":null},\"properties\":{\"prop2\":true,\"prop1\":\"CUSTOM_PARAM_VALUE\",\"prop3\":3}}";
        self.assertIsNotNone(body)
        self.assertEqual(body, expected)


if __name__ == '__main__':
    unittest.main()
