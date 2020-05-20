import json
import logging
import uuid
from datetime import datetime
import asyncio

from azure.iot.device import Message
# pylint: disable=E0611
from azure.iot.device.aio import IoTHubModuleClient


class Publisher:
    """
    The publisher can dump dictionaries to a json-string and send this string as a message to the specified
    target module
    """

    def __init__(self, module_name, output_name):
        """
        Create a new publisher to send values to the iot hub
        :param module_name: Name of the module as str
        :param output_name: The name of the output queue as str
        """
        self.module_name = module_name
        self.output_name = output_name
        self.module_client = IoTHubModuleClient.create_from_edge_environment()
        self.last_sent_values = dict()
        self.datetime_last_message = None
        self.input_listeners = []
        logging.log(logging.DEBUG, "Setup publisher for module %s" % module_name)

    async def _create_message(self, module_name, values) -> Message:
        """
        Creates the message with the values to forward to the output.
        :param module_name: Name of the module
        :param values: The values as dict which have to be forwarded
        """
        values["moduleName"] = module_name
        values["time"] = str(datetime.now())
        message = Message(bytearray(json.dumps(values), 'utf-8'))
        message.message_id = str(uuid.uuid4())
        return message

    async def send_message(self, values, output=None):
        """
        Forwards the message to the output.
        :param values: The values as dict which have to be forwarded
        :param output: The name of the output queue (if set to none: use the default output name)
        """
        output_queue = self.output_name if output is None else output
        logging.log(logging.DEBUG, "Sending values:  %s" % json.dumps(values))
        message = await self._create_message(self.module_name, values)
        await self.module_client.send_message_to_output(message, output_queue)
        self.last_sent_values = values
        self.datetime_last_message = datetime.now()

    def register_input_listener(self, input_listener):
        """
        Registers a input listener which must be called when a message with the specified input queue name of the listener arrives.
        :param input_listener: The input listener which must be called
        """
        logging.log(logging.DEBUG,
                            "Registered a new input listener at module: %s" % self.module_name)
        self.input_listeners.append(input_listener)

    async def start_input_listeners(self, stop_listeners=None):
        """
        Starts listening at the registered input listeners.
        :param stop_listeners: The callback function to define the behavior for halting the input listeners
        """
        logging.log(logging.DEBUG,
                            "Started all registered listeners at module: %s" % self.module_name)
        await self.module_client.connect()
        if stop_listeners is not None:
            listeners = asyncio.gather(*self.input_listeners)
            loop = asyncio.get_event_loop()
            user_finished = loop.run_in_executor(None, stop_listeners)
            await user_finished
        else:
            listeners = await asyncio.gather(*self.input_listeners)
        listeners.cancel()
        await self.module_client.disconnect()