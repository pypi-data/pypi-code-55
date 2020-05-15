from typing import Dict

import json
import time
import random
import traceback

from petisco.logger.interface_logger import INFO, ERROR
from petisco.events.event import Event
from functools import wraps
from meiga import Result
from meiga.decorators import meiga

from petisco.logger.log_message import LogMessage


DEFAULT_LOGGER = None


class _SubscriberHandler:
    def __init__(
        self,
        logger=DEFAULT_LOGGER,
        message_broker: str = "rabbitmq",
        filter_routing_key: str = None,
        delay_after: float = None,
        percentage_simulate_nack: float = None,
    ):
        """
        Parameters
        ----------
        logger
            A ILogger implementation. Default NotImplementedLogger
        message_broker:
            Select Message Broker. For now, only available rabbitmq
        filter_routing_key:
            Only process, if received message is equal to given filter_routing_key
        delay_after:
            Delay ack or reject for a given number of seconds.
        percentage_simulate_nack:
            Percentage of simulate nack when the result is a success. [0.0 -> 1.0]. Where 1.0 rejects all the events.

        """
        self.logger = logger
        if message_broker != "rabbitmq":
            raise TypeError(
                f"Petisco Subscriber: message broker {message_broker} is not implemented. Try with rabbitmq"
            )
        self.filter_routing_key = filter_routing_key
        self.delay_after = delay_after
        self.percentage_simulate_nack = percentage_simulate_nack

    def _check_logger(self):
        if self.logger == DEFAULT_LOGGER:
            from petisco import Petisco

            self.logger = Petisco.get_logger()

    def _nack_simulation(self):
        if self.percentage_simulate_nack is None:
            return False
        else:
            return (
                self.percentage_simulate_nack
                and random.random() < self.percentage_simulate_nack
            )

    def _log_nack_simulation(self, log_message: LogMessage):
        self.logger.log(
            INFO,
            log_message.set_message(
                f"Message rejected (Simulation rejecting {self.percentage_simulate_nack * 100}% of the messages)"
            ),
        )

    def _filter_by_routing_key(self, routing_key: str):
        if self.filter_routing_key is None:
            return False
        else:
            return self.filter_routing_key != routing_key

    def _log_filter_by_routing_key(self, log_message: LogMessage):
        self.logger.log(
            INFO,
            log_message.set_message(
                f"Message rejected (filtering by routing_key {self.filter_routing_key})"
            ),
        )

    def _log_invalid_event_format(self, log_message: LogMessage, body: Dict):
        self.logger.log(INFO, log_message.set_message(f"Invalid event format: {body})"))

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @meiga
            def run_controller(*args, **kwargs) -> Result:
                return func(*args, **kwargs)

            self._check_logger()

            ch, method, properties, body = args

            log_message = LogMessage(layer="subscriber", operation=f"{func.__name__}")

            self.logger.log(
                INFO,
                log_message.set_message(
                    {"routing_key": method.routing_key, "body": json.loads(body)}
                ),
            )

            if self._nack_simulation():
                ch.basic_nack(delivery_tag=method.delivery_tag)
                self._log_nack_simulation(log_message)
                return

            if self._filter_by_routing_key(method.routing_key):
                ch.basic_nack(delivery_tag=method.delivery_tag)
                self._log_filter_by_routing_key(log_message)
                return

            try:
                event = Event.from_json(body)
            except TypeError:
                event = Event.from_deprecated_json(body)
            except:  # noqa E722
                self._log_invalid_event_format(log_message, body)
                return ch.basic_nack(delivery_tag=method.delivery_tag)

            result = run_controller(event)

            if self.delay_after:
                time.sleep(self.delay_after)

            if result is None or result.is_failure:
                message = f"{result}: {traceback.format_exc()}"
                self.logger.log(ERROR, log_message.set_message(message))
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        return wrapper


subscriber_handler = _SubscriberHandler
