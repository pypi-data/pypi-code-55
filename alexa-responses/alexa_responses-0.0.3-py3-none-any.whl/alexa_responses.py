import json


class AlexaResponses:
    def __init__(self, skill_name, locale="en-US", languages="languages.json"):
        self.name = skill_name
        self.languages = languages
        self.set_locale(locale)

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
        with open(self.languages) as f:
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
