import json
import time
import uuid


class AlexaResponses:
    def __init__(self, skill_name, locale="en-US"):
        self.name = skill_name
        with open("languages.json") as f:
            data = json.loads(f.read())
            if locale in data.keys():
                self.lang = data[locale]
            else:
                raise ValueError("Unknown locale")

    def get_slot_id(self, intent, name):
        slots = intent["slots"]
        if name not in slots:
            return None
        if "resolutions" not in slots[name]:
            return None
        resolutions = slots[name]["resolutions"]["resolutionsPerAuthority"]
        if not resolutions:
            return None
        return resolutions[0]["values"][0]["value"]["id"]

    def get_slot_value(self, intent, name):
        slots = intent["slots"]
        if name not in slots:
            return None
        return slots[name].get("value")

    def set_locale(self, locale):
        with open("languages.json") as f:
            data = json.loads(f.read())
            if locale in data.keys():
                self.lang = data[locale]
            else:
                raise ValueError("Unknown locale")

    def _build_response(self, session_attributes, speechlet_response):
        return {
            "version": "1.0",
            "sessionAttributes": session_attributes,
            "response": speechlet_response,
        }

    def welcome(self, end_session=True):
        response = {"outputSpeech": {"type": "SSML", "ssml": self.lang["WELCOME"]}}
        if self.lang["WELCOME2"]:
            response["reprompt"] = {
                "outputSpeech": {"type": "SSML", "text": self.lang["WELCOME2"]}
            }
        response["shouldEndSession"] = end_session
        return self._build_response({}, response)

    def help(self):
        response = {"outputSpeech": {"type": "SSML", "ssml": self.lang["HELP"]}}
        response["shouldEndSession"] = False
        return self._build_response({}, response)

    def intent(self, output=None, reprompt=None, card=None, end_session=True, data={}):
        response = {}
        if output:
            if self.lang[output].startswith("<speak>"):
                response["outputSpeech"] = {
                    "type": "SSML",
                    "ssml": self.lang[output].format(**data),
                }
            else:
                response["outputSpeech"] = {
                    "type": "PlainText",
                    "text": self.lang[output].format(**data),
                }
        if reprompt:
            response["reprompt"] = {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": self.lang[reprompt].format(**data),
                }
            }
        response["shouldEndSession"] = end_session
        return self._build_response({}, response)

    def end_request(self):
        response = {
            "outputSpeech": {"type": "PlainText", "text": self.lang["BYE"]},
            "shouldEndSession": True,
        }
        return self._build_response({}, response)

    def permissions_card(self, permissions):
        response = {
            "outputSpeech": {"type": "PlainText", "text": self.lang["PERMISIONS"]},
            "card": {"type": "AskForPermissionsConsent", "permissions": permissions},
        }
        return self._build_response({}, response)


class AlexaSmartHome:
    def __init__(self, locale="en-US"):
        self.set_locale(locale)

    def set_locale(self, locale):
        with open("languages.json") as f:
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
