import json
import unittest
from unittest.mock import MagicMock, patch
import time

from spuhllib.edgemessages import Publisher

class PublisherTest(unittest.TestCase):

    @patch('spuhllib.edgemessages.publisher.IoTHubModuleClient')
    def setUp(self, iot_hub_module_client):
        self.module_name = "module name"
        self.output_name = "output name"
        self.module_client = MagicMock()
        iot_hub_module_client.create_from_edge_environment.return_value = self.module_client
        self.publisher = Publisher(self.module_name, self.output_name)
        self.iot_hub_module_client_mock = iot_hub_module_client

    def test_init(self):
        self.iot_hub_module_client_mock.create_from_edge_environment.assert_called_once()
        self.assertIsNotNone(self.publisher.last_sent_values)
        self.assertIsNone(self.publisher.datetime_last_message)

    @patch('spuhllib.edgemessages.publisher.Message')
    @patch('spuhllib.edgemessages.publisher.datetime')
    async def test_send_message(self, datetime_mock, iot_hub_message_mock):
        message_mock = MagicMock()
        iot_hub_message_mock.return_value = message_mock
        datetime_now = "2019-12-02 18:35:58.451694"
        datetime_mock.now.return_value = datetime_now
        values = {"temperature": 20}
        self.publisher.send_message(values)
        self.module_client.send_message_to_output.assert_called_with(message_mock, self.output_name)
        self.assertEqual(values, self.publisher.last_sent_values)
        self.assertEqual(datetime_now, self.publisher.datetime_last_message)

    @patch('spuhllib.edgemessages.publisher.Message')
    @patch('spuhllib.edgemessages.publisher.uuid')
    async def test_create_message_uuid(self, uuid_mock, message_mock):
        uuid4_str = "cf870b1e-6cae-41ca-b6a1-af118e319a11"
        uuid_mock.uuid4.return_value = uuid4_str
        message = await self.publisher._create_message("temperatureModule", {"temperature": 20})
        message_mock.assert_called()
        uuid_mock.uuid4.assert_called_once()
        self.assertEqual(uuid4_str, message.message_id)

    @patch('spuhllib.edgemessages.publisher.datetime')
    async def test_create_message_time(self, datetime_mock):
        datetime_now = "2019-12-02 18:35:58.451694"
        datetime_mock.now.return_value = datetime_now
        message = await self.publisher._create_message("temperatureModule", {"temperature": 20})
        result = message.data.decode('utf-8')
        expected = json.dumps({"temperature": 20, "moduleName": "temperatureModule", "time": datetime_now})
        self.assertEqual(expected, result)
        datetime_mock.now.assert_called_once()

    def test_register_input_listener(self):
        input_listener = MagicMock()
        self.publisher.register_input_listener(input_listener)
        self.assertEqual(self.publisher.input_listeners[0], input_listener)