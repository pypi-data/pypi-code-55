import jsonschema
from salesfly.multipart import encode


class MailAPI(object):
    """
    Mail API
    """
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def send(self, message):
        jsonschema.validate(message, schema=schema)
        files = []
        if "attachments" in message.keys():
            files = message["attachments"]  # take out of message
            message["attachments"] = {}     # clear
        body, headers = encode(message, files)
        return self.rest_client.post("/v1/mail/send", body, headers)


##################################################################################################
# Message schema definition:
schema = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date-time"},
        "from": {"type": "string"},
        "from_name": {"type": "string", "maxLength": 50},
        "to": {
            "type": "array",
            "minLength": 1,
            "maxLength": 50,
            "items": {"type": "string", }
        },
        "cc": {
            "type": "array",
            "minLength": 1,
            "maxLength": 50,
            "items": {
                "type": "string"
            }
        },
        "bcc": {
            "type": "array",
            "minLength": 1,
            "maxLength": 50,
            "items": {
                "type": "string"
            }
        },
        "reply_to": {
            "type": "string",
            "maxLength": 50
        },
        "subject": {
            "type": "string",
            "maxLength": 100
        },
        "text": {"type": "string"},
        "html": {"type": "string"},
        "attachments": {
            "type": "array",
            "maxLength": 10,
            "items": {
                "type": "string"
            }
        },
        "tags": {
            "type": "array",
            "maxLength": 3,
            "items": {
                "type": "string",
                "maxLength": 20,
            }
        },
        "charset": {
            "type": "string",
            "maxLength": 20
        },
        "encoding": {
            "type": "string",
            "maxLength": 20
        },
        "require_tls": {
            "type": "boolean"
        },
        "verify_cert": {
            "type": "boolean"
        },
        "open_tracking": {
            "type": "boolean"
        },
        "click_tracking": {
            "type": "boolean"
        },
        "text_click_tracking": {
            "type": "boolean"
        },
        "unsubscribe_tracking": {
            "type": "boolean"
        },
        "test_mode": {
            "type": "boolean"
        }
    },
    "required": ["from", "to", "subject", "text"],
    "additionalProperties": False
}
