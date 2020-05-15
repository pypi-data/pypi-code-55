"""
Abstraction to access emails received by a SMTP4dev instance.

A way to programmatically access emails received on a SMTP4dev
host easily. See the [SMTP4dev](https://github.com/rnwood/smtp4dev)
documentation for more info.
"""

import requests

from .message import Message


class ApiError(BaseException):
    """
    An error during an API call
    """


class Smtp4Dev:
    """
    API client for SMTP4dev.
    """

    def __init__(self, base_url):
        """
        Client for a SMTP4dev instance.
        :param base_url: the base URL to access the smtp4dev. No final /.
        :raises: ApiError
        """
        self.base_url = base_url + '/api/Messages'

    def list_messages(self, unread_only=False):
        """
        List all messages in the smtp4dev inbox.
        :param unread_only: Only retrieve the unread messages
        :returns: a generator of Message items
        :raises: ApiError
        """
        response = requests.get(
            f"{self.base_url}?sortColumn=receivedDate&sortIsDescending=true"
        )
        if response.status_code != 200:
            raise ApiError()

        if unread_only:
            return (Message.deserialize(m) for m in response.json() if m["isUnread"])
        return (Message.deserialize(m) for m in response.json())

    def mark_message_read(self, msg_id):
        """
        Mark a message a read in the inbox.
        :param msg_id: the message's pk (a UUID)
        :raises: ApiError
        """
        response = requests.post(f"{self.base_url}/{msg_id}", data="")
        if response.status_code != 200:
            raise ApiError()

    def get_message(self, msg_id):
        """
        Retrieve a specific message by ID.
        :param msg_id: the messages's pk (a UUID)
        :returns: a Message instance
        :raises: ApiError
        """
        response = requests.get(f"{self.base_url}/{msg_id}")
        if response.status_code != 200:
            raise ApiError()

        body = self._get_message_body(msg_id)
        self.mark_message_read(msg_id)

        return Message.deserialize(response.json(), html=body)

    def _get_message_body(self, msg_id):
        response = requests.get(f"{self.base_url}/{msg_id}/html")
        if response.status_code != 200:
            raise ApiError()

        return response.content
