#  Copyright (c) 2020 Netflix.
#  All rights reserved.
import random
import string
from threading import Lock
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import arrow
import bugsnag
from kaiju_mqtt_py import KaijuMqtt
from kaiju_mqtt_py.sslconfigmanager import SslConfigManager

# Implementation libs
from ntscli_cloud_lib.device_identifier import DeviceIdentifier
from ntscli_cloud_lib.log import logger
from ntscli_cloud_lib.mqtt_retryable_error import MqttRetryableError
from ntscli_cloud_lib.retry_with_backoff import retry
from ntscli_cloud_lib.testplan_checker import TestPlanChecker

CLOUD_BROKER_NAME = "cloud"
NTSCLI_KEY = "ntscli"
RESPONSE_KEY = "response"


def make_explicit_batch_id() -> str:
    """
    Make a string to use as a shared batch ID across multiple runs.

    ntscli-${utils.randomString(8)} -${new Date().toISOString()}
    Example from something on my screen:
    "lastBatch":"ntscli-GT5FDI3F-2020-04-20T16:07:21.063Z"

    fbrennan: Its a free form string that can't contain '+' or '#' chars
    """
    randstr = ("".join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])).upper()  # nosec B311  not used for crypto
    datestr = arrow.utcnow().isoformat().replace("+00:00", "Z")
    return f"ntscli-{randstr}-{datestr}"


class Session:
    """
    A stateful connection to the AWS IoT broker for communicating with mqtt-router.

    This object only tracks state surrounding the KaijuMqtt connection.
    """

    iot_base_pattern: str = "client/partner/{}"  # provide certificate id with str.format()

    def __init__(self):
        """Constructor."""
        self.kaiju: KaijuMqtt = KaijuMqtt()
        self.cleanup_funcs: List = []
        self.cloud_topic_format: bool = False
        # this is the intended rae target in the format r3000123 so we can for topics with it
        self.rae_topic_string: Optional[str] = None
        self.connection_lock: Lock = Lock()

    def _topic_with_session_id(self, command: str) -> str:
        """
        Form a topic with the session ID embedded.

        This is only possible after the ssl configuration has been loaded, which is typically during
        the connect() call.

        :param command: The test_runner subcommand to add
        :return:
        """
        # also provide command
        if self.kaiju.certificate_id == "":
            raise ValueError(
                "The connection has not been made yet, so we can't form the topic string. "
                "This is a programming bug, so please contact Netflix."
            )
        return (Session.iot_base_pattern + "/test_runner/{}").format(self.kaiju.certificate_id, command)

    def connect(self, broker: str = CLOUD_BROKER_NAME) -> None:
        """
        Connect the underlying broker.

        The client should explicitly call mysession.destructor() to clean up.

        If the configuration for the broker configuration named is missing or incorrect, an error will be thrown.

        :return: None
        """
        manager = SslConfigManager()
        logger.debug(f"Looking for configuration {broker}")
        if not manager.has(broker):
            logger.debug(f"Could not find configuration {broker}, raising ValueError.")
            raise ValueError(
                "The SSL configuration for the named broker is missing. " "Check the ~/.config/netflix/ directory for configurations."
            )
        config = manager.get(broker)
        if not config.iscomplete():
            logger.debug(f"Configuration {broker} incomplete, raising ValueError.")
            raise ValueError(
                "The SSL configuration for the named broker is incomplete. "
                "Check the ~/.config/netflix/ directory for configurations. "
                "Please download it again from the Netflix partner portal."
            )
        with self.connection_lock:
            self.kaiju.connect(broker)

    def subscribe(self, topic: str, newfunc: Callable, options_dict: Dict = None) -> None:
        """
        Subscribe to a topic on the MQTT broker.

        This typically would be used to subscribe to the status stream of a test plan.

        The signature of the new function should be:
        def handle_updates(client, userdata, packet):
            ...

        This is the normal shape for a paho-mqtt topic message subscriber. The most interesting arg is packet.payload,
        of type dict. The packet.payload is a list of dicts. The dicts start out with the following keys:
        url, status, name logfile, step
        These will be populated with the current state of the test run. This will get called typically whenever one of
        the elements changes its value in the Automator module.
        Additional keys are added as the Automator is notified of new information about a test.

        :param topic:
        :param newfunc:
        :param options_dict:
        :return:
        """
        options = options_dict if options_dict else {"qos": 1, "timeoutMs": 15000}
        cleanup = self.kaiju.subscribe(topic, newfunc, options)

        self.cleanup_funcs.append(cleanup)

    def get_test_plan_for_device(self, device: DeviceIdentifier) -> Dict:
        """
        Request a test plan from the remote server.

        This is returned as a JSON dict.

        Example response:
        {"branch": "5.1",
        "testcases": [
                {"exec": "/tests/suite/file1.js?args"},
                {"exec": "/tests/suite/file2.js?args"},
                ...
            ],
        "sdkVersion": "ninja_6",
        }

        To run this plan, it needs to be put in the following structure:
        { "target": {...},
          "testplan" : [this object] }

        :param device: The DeviceIdentifier to use in the data section of the request.
        :return: The response from the Automator module as a dict.
        """
        topic = self._topic_with_session_id("get_testplan")
        response = self.kaiju.request(topic, device.as_dict(), options={"qos": 1, "timeoutMs": 3 * 60 * 1000})
        if response["status"] != 200 or "testcases" not in response["body"]:
            # if the automator sent back a message, we were connected
            if "message" not in response["body"]:
                self.check_broker()

            err = "Error in get_test_plan response"
            toreport = ValueError(err)
            bugsnag.notify(
                toreport,
                meta_data={
                    NTSCLI_KEY: {
                        "target": device.as_dict(),
                        "broker": self.kaiju.client._host,
                        "certificate_id": self.kaiju.certificate_id,
                    },
                    RESPONSE_KEY: response,
                },
            )

        return response

    def check_broker(self):
        """
        Use a self-responder to check whether the broker is responding.

        This is used if a call fails and we want to make sure the broker is responding, even if the remote service is
        not.

        It does create a new, separate Session/connection during the check.
        """
        from ntscli_cloud_lib.self_responder import SelfResponder

        responder = SelfResponder()
        try:
            responder.start(self.kaiju.client._host)
            responder.check_request()
        except ValueError:
            err = "Unable to send and receive messages to remote broker"
            toreport = ValueError(err)
            bugsnag.notify(
                toreport, meta_data={NTSCLI_KEY: {"broker": self.kaiju.client._host, "certificate_id": self.kaiju.certificate_id}}
            )
        finally:
            responder.stop()

    @retry((MqttRetryableError,))
    def run_plan(self, plan: Dict, check: bool = False) -> Dict:
        """
        Send a request to run a specified test plan.

        If called with check=True, this will do a basic sanity check on the test plan for general shape before submitting, because it
        is easy to create malformed JSON. If there is a problem with the plan's format, SyntaxError will be raised before sending over MQTT.

        A request needs to be formed around the results of a call to get_test_plan_for_device before
        calling this. It should be shaped like this:
        { "target": {"ip", "192.168.x.y", "rae", "r3000123"},
          "testplan" : [test plan object from get_test_plan_for_device]}

        Be sure to note the batch ID reported at log level WARNING or in the response JSON if you want to find the batch without visiting
        the web UI.

        :param check: If true, throw a SyntaxError if the test fails to pass a basic sanity check.
        :param plan: The plan to execute.
        :return: The response from the Automator module as a dict.
        """
        if check and not TestPlanChecker.sanity_check(plan):
            err = "The request failed basic sanity checks."
            toreport = SyntaxError(err)
            target = "unset"
            if "target" in plan:
                target = plan["target"]
            bugsnag.notify(
                toreport,
                meta_data={NTSCLI_KEY: {"target": target, "broker": self.kaiju.client._host, "certificate_id": self.kaiju.certificate_id}},
            )
            logger.critical(err)
            raise toreport

        topic = self._topic_with_session_id("run_tests")
        logger.debug(f"Preparing to post to topic: {topic}")

        response = self.kaiju.request(topic, plan, {"qos": 1, "timeoutMs": 60 * 1000})
        # Detect and report on fail states
        if "body" in response and "message" in response["body"] and "Executing testplan on target." not in response["body"]["message"]:
            if "Device is currently busy" in response["body"]["message"]:
                # busy message looks similar to this:
                # {'status': 200,
                # 'body': {'status': 'running', 'message':
                #          'Device is currently busy running tests, request test cancellation or try again later'}}
                logger.info("The device reports that it is busy.")
                raise MqttRetryableError(
                    "The automator thinks the device has been busy for about a minute and 4 separate requests. You may "
                    "choose to wait, or cancel the current test plan before this request can succeed."
                )

            elif "Failed to lookup" in response["body"]["message"]:
                """ The not-found-device message looks like this:
                {'status': 200, 'body':
                {'message': 'Failed to lookup device based on the data provided, please double check data,
                launch Netflix and try again', 'error': 'Error: Failed to lookup device based on the data provided,
                please double check data, launch Netflix and try again ... (stack trace)'}}
                """
                err = "The RAE could not locate the device identifier"
                toreport = ValueError(err)
                bugsnag.notify(
                    toreport,
                    meta_data={
                        NTSCLI_KEY: {
                            "target": plan["target"],
                            "broker": self.kaiju.client._host,
                            "certificate_id": self.kaiju.certificate_id,
                        },
                        RESPONSE_KEY: response["body"]["message"],
                    },
                )
                logger.error("The RAE does not recognize the device identifier:\n{}".format(response["body"]["message"]))
                raise ValueError("The RAE does not recognize the device identifier:\n{}".format(response["body"]["message"]))

            err = "The automator rejected the request to run tests"
            toreport = ValueError(err)
            bugsnag.notify(
                toreport,
                meta_data={
                    NTSCLI_KEY: {"target": plan["target"], "broker": self.kaiju.client._host, "certificate_id": self.kaiju.certificate_id},
                    RESPONSE_KEY: response,
                },
            )
            raise ValueError("The automator rejected the request to run tests:\n{}".format(response["body"]["message"]))

        if "body" in response and "batch_id" in response["body"]:
            logger.warning(f'Scheduled batch ID {response["body"]["batch_id"]}')

        return response

    def cancel_plan_for_device(self, device: DeviceIdentifier) -> Dict:
        """
        Request that we cancel the tests for this device.

        :param device: Which device to cancel for.
        :return: dict with keys status and body. Status will be a typical HTTP error code.
        """
        topic = self._topic_with_session_id("cancel_tests")
        response = self.kaiju.request(topic, device.as_dict())
        return response

    def destructor(self):
        """
        Cleanly shut down the KaijuMqtt object and disconnect.

        Some unsubscribe actions need to be performed on shutdown of the client. I'd suggest putting this in a finally:
        clause to prevent strange behaviors. It is safe to call this multiple times.

        :return:
        """
        [x() for x in self.cleanup_funcs]
        with self.connection_lock:
            self.kaiju.close()

    def get_eyepatch_connected_esn_list(self, rae: str) -> List[str]:
        """
        Get the list of devices for which an EyePatch is connected.

        from v 1.1
        Abstracted due to the intent to change the implementation later.

        :param rae: The RAE to request the list of connected devices from. Requires the EyePatch module to be installed.
        :return: list of strings, which are the ESNs with detected eyepatch configurations.
        """
        avaf_peripheral_list_topic = Session.iot_base_pattern.format(self.kaiju.certificate_id) + "/avaf/execute/peripheral.list"
        reply: Dict = self.kaiju.request(avaf_peripheral_list_topic, {"type": "eyepatch", "target": {"rae": rae}})
        if "body" not in reply:
            toreport = ValueError("There was no body in the response to the peripheral list request.")
            bugsnag.notify(toreport, meta_data={NTSCLI_KEY: {"rae": rae}, RESPONSE_KEY: reply})
            raise toreport
        if type(reply["body"]) is not list:
            bugsnag.notify(
                ValueError("The peripheral list API did not include a list of peripherals."),
                meta_data={
                    NTSCLI_KEY: {"rae": rae, "broker": self.kaiju.client._host, "certificate_id": self.kaiju.certificate_id},
                    RESPONSE_KEY: reply,
                },
            )
            logger.error("The peripheral list API did not include a list of peripherals.")
            logger.error(reply["body"])
            return []
        returnme: List[str] = [peripheral["esn"] for peripheral in reply["body"] if peripheral["esn"] != ""]
        return returnme

    def is_esn_connected_to_eyepatch(self, rae: str, esn: str) -> bool:
        """
        Convenience call to just find out if the ESN I'm interested in is in that list.

        from v 1.1
        Note that it makes a request to the RAE on every call, as there's no great way to determine cache status or
        valid duration.

        This is not using the DeviceIdentifier because we're not yet assured that the other fields will remain queryable long term.

        :param esn: The ESN of the device we are interested in. Note that this is not using the DeviceIdentifier.
        :param rae: The RAE to request the list of connected devices from. Requires the EyePatch module to be installed.
        :return:
        """
        return esn in self.get_eyepatch_connected_esn_list(rae)

    def status(self, rae: str, **kwargs) -> Dict:
        """Get status."""
        """
        Get the state of in-memory Automator sessions.

        These are cleared any time the Automator service restarts. The result object includes the most recent topic to subscribe to for
        the specified device.

        A request with no device identifier should get the state of all sessions.

        This returns data in one of three shapes:
        If a session is not running you would see:

        {
            'status': 200,
            'body': {'sessions':
                [
                    {'status': 'idle',  # or running, cancelling
                     'target': {
                        'ip': '192.168.144.14',
                        'usbId': '04202160095330000385',
                        'macAddress': '00:04:4B:55:F6:24',
                        'esn': 'NFANDROID2-PRV-SHIELDANDROIDTV-NVIDISHIELD=ANDROID=TV-15894-'
                               'B870830DB5F845A545A34A536B73E1D186852F3305237B999319ED128B635374'
                     },
                     'lastBatch': 'ntscli-6BS9WP06-2020-03-30T20:32:57.423Z'
                    }
                ]
            }
        }

        If it is running currently, you get the key "resultTopic" instead of "lastBatch", and that will be the topic
        you can subscribe to for live monitoring.

        Example replies:

        idle and nothing having run before - after reboot probably:
        {'status': 200, 'body': {'sessions': []}}

        running:
        {'status': 200, 'body': {'sessions': [{'status': 'running', 'target': {'ip': '192.168.144.54',
        'usbId': '0323618087338', 'macAddress': '00:04:4B:B8:39:D8', 'esn': '[esn]'},
        'resultTopic': 'cloud/partner/yourCertId/more/opaque_stuff'
        }]}}

        finished:
        {'status': 200, 'body': {'sessions': [{'status': 'idle', 'target': {'ip': '192.168.144.54',
        'usbId': '0323618087338', 'macAddress': '00:04:4B:B8:39:D8', 'esn': '[esn]'},
        'lastBatch': 'ntscli-6BS9WP06-2020-03-30T20:32:57.423Z'}]}}

        The final response format includes the results list. To get this format, you must make the
        request with both a DeviceIdentifier (so A. mqtt-router knows where to route the message, and B. so Automator knows which device
        to qualify the batch_id in), and the batch ID. If any part is missing, you might get just the Automator-session status block.

        This payload includes the state of all the tests at key "results". The format of that is described next.

        The result list is a list of Dicts. Each describes the state of a test.
        The keys for an unstarted test start as:
        name, url, status

        The key 'status' is one of these:
        running, pending, passed, failed, cancelled, invalid

        Once the status goes to "running" it will get a couple more keys (not all at once):
        logfile, step

        Once it's ended in some form, you might get "error_state" as well as some log entry keys.

        Most interestingly, you can deduce your progress by measuring the index of the currently running index vs.
        the length of full_payload:

        # only somewhat accurate X of Y type of thing
        total = len(full_payload)
        pending_list = [1 for elt in full_payload if elt["status"] == "pending"]
        done = total - sum(pending_list)

        running = [elt["name"] + ':' + elt["step"].split(",")[0]
            for elt in full_payload
            if elt["status"] == "running"
            if "step" in elt
        ]

        :param rae: the target rae to get status from, example r3000123
        :param kwargs: device=DeviceIdentifier(...) - an optional device to attempt a match on. The rae field in this object is ignored.
        :return:
        """
        device: DeviceIdentifier = kwargs.get("device", None)
        batch_id: str = kwargs.get("batch_id", None)

        request: Dict = {}
        if device is not None:
            request.update(device.as_dict())
        if "target" not in request or "rae" not in request["target"]:
            request.update({"target": {"rae": rae}})
        if batch_id is not None:
            request.update({"batch_id": batch_id})
        topic = self._topic_with_session_id("status")
        return self.kaiju.request(topic, request, {"qos": 1, "timeoutMs": 15000})

    def get_result_for_batch_id(self, device: DeviceIdentifier, batch_id: str):
        """
        Get the result block for a specified batch ID.

        Technically you can do this with status, but it's fiddly enough to warrant a convenience call.
        """
        return self.status(device=device, rae=device.rae, batch_id=batch_id)

    def get_device_list(self, rae: str) -> List[DeviceIdentifier]:
        """
        Get the list of known devices behind the Automator.

        :return:
        """
        request: Dict = {"target": {"rae": rae}}
        topic = self._topic_with_session_id("list_targets")
        resp = self.kaiju.request(topic, request, {"qos": 1, "timeoutMs": 15000})
        if "body" not in resp or resp["status"] != 200 or "error" in resp["body"]:
            bugsnag.notify(
                ValueError("Failed to get device list"),
                meta_data={
                    NTSCLI_KEY: {"rae": rae, "broker": self.kaiju.client._host, "certificate_id": self.kaiju.certificate_id},
                    RESPONSE_KEY: resp,
                },
            )
            return []
        return [DeviceIdentifier(**elt, rae=rae) for elt in resp["body"]]
