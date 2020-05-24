import json
import time
import uuid


class AlexaSmartHome:
    def __init__(self, locale="en-US", languages="languages.json"):
        self.languages = languages
        self.set_locale(locale)

    def set_locale(self, locale):
        with open(self.languages) as f:
            data = json.loads(f.read())
            if locale in data.keys():
                self.lang = data[locale]
            else:
                raise ValueError("Unknown locale")

    def discovery(self, directive, endpoints):
        return {
            "event": {
                "header": {
                    "namespace": "Alexa.Discovery",
                    "name": "Discover.Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                },
                "payload": {
                    "scope": {
                        "type": "BearerToken",
                        "token": directive["payload"]["scope"]["token"],
                    },
                    "endpoints": endpoints,
                },
            }
        }

    def power_response(self, action, endpoint, correlationToken):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.PowerController",
                        "name": "powerState",
                        "value": action,
                        "timeOfSample": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()
                        ),
                        "uncertaintyInMilliseconds": 500,
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def range_response(self, action, instance, endpoint, correlationToken):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.RangeController",
                        "name": "rangeValue",
                        "instance": instance,
                        "value": action,
                        "timeOfSample": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()
                        ),
                        "uncertaintyInMilliseconds": 5000,
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def mode_response(self, instance, value, directive):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.ModeController",
                        "instance": instance,
                        "name": "mode",
                        "value": value,
                        "timeOfSample": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()
                        ),
                        "uncertaintyInMilliseconds": 5000,
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": directive["header"]["correlationToken"],
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": directive["payload"]["scope"]["token"],
                    },
                    "endpointId": endpoint,
                },
                "payload": {},
            },
        }

    def mode_state_response(self, instance, action, uncertainty=1000):
        return {
            "namespace": "Alexa.ModeController",
            "instance": instance,
            "name": "mode",
            "value": action,
            "timeOfSample": time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()),
            "uncertaintyInMilliseconds": 0,
        }

    def state_report_response(self, properties, directive):
        return {
            "context": {"properties": properties},
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "StateReport",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": directive["header"]["correlationToken"],
                },
                "endpoint": {"endpointId": directive["endpoint"]["endpointId"]},
                "payload": {},
            },
        }

    def temperature_status_response(self, value, scale="CELSIUS", uncertainty=60000):
        return {
            "namespace": "Alexa.TemperatureSensor",
            "name": "temperature",
            "value": {"value": value, "scale": scale},
            "timeOfSample": time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()),
            "uncertaintyInMilliseconds": uncertainty,
        }

    def range_status_response(self, instance, value, uncertainty=10000):
        return {
            "namespace": "Alexa.RangeController",
            "name": "rangeValue",
            "instance": instance,
            "value": value,
            "timeOfSample": time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()),
            "uncertaintyInMilliseconds": uncertainty,
        }

    def health_status_response(self, value="OK", uncertainty=10000):
        return {
            "namespace": "Alexa.EndpointHealth",
            "name": "connectivity",
            "value": {"value": "OK"},
            "timeOfSample": time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()),
            "uncertaintyInMilliseconds": uncertainty,
        }

    def channel_response(self, value, endpoint, correlationToken):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.ChannelController",
                        "name": "channel",
                        "value": {"number": value},
                        "timeOfSample": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()
                        ),
                        "uncertaintyInMilliseconds": 0,
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def input_response(self, value, endpoint, correlationToken):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.InputController",
                        "name": "input",
                        "value": value,
                        "timeOfSample": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()
                        ),
                        "uncertaintyInMilliseconds": 0,
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def playback_response(self, value, endpoint, correlationToken):
        return {
            "context": {"properties": []},
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def speaker_response(self, volume, muted, endpoint, correlationToken):
        return {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.Speaker",
                        "name": "volume",
                        "value": volume,
                        "timeOfSample": "2017-02-03T16:20:50.52Z",
                        "uncertaintyInMilliseconds": 0,
                    },
                    {
                        "namespace": "Alexa.Speaker",
                        "name": "muted",
                        "value": muted,
                        "timeOfSample": "2017-02-03T16:20:50.52Z",
                        "uncertaintyInMilliseconds": 0,
                    },
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlationToken,
                },
                "endpoint": {"endpointId": endpoint},
                "payload": {},
            },
        }

    def error(self, type_, msg, data={}):
        return {
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "ErrorResponse",
                    "messageId": str(uuid.uuid4()),
                    "payloadVersion": "3",
                },
                "endpoint": {"endpointId": "INVALID"},
                "payload": {"type": type_, "message": self.lang[msg].format(**data)},
            }
        }
