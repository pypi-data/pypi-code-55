#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: Azure Queues
"""

import datetime as datetime
import json

from taz.storage_account import StorageAccount
from azure.core.exceptions import ResourceExistsError

from azure.storage.queue import QueueClient, QueueMessage


class Queue:
    def __init__(self, name: str, storage_account: StorageAccount):
        """Queue constructor

        :param name: queue name
        :type name: str
        :param storage_account: storage account object
        :type storage_account: StorageAccount
        """
        self.name = name
        self.storage_account = storage_account
        self.client = QueueClient.from_connection_string(
            storage_account.connection_string, self.name
        )

    def create(self):
        """create queue
        do not raise an exception if exists

        :return: self
        :rtype: Queue
        """
        try:
            self.client.create_queue()
        except ResourceExistsError:
            pass

        return self

    def delete(self):
        """delete queue
        raises an exception if does not exists

        :return: self
        :rtype: Queue
        """
        self.client.delete_queue()
        return self

    def send(self, msg: str):
        """send a message

        :param msg: message to send
        :type msg: str
        :return: self
        :rtype: Queue
        """
        self.last_sent_message = self.client.send_message(msg)
        return self

    def get_last_sent_message(self) -> QueueMessage:
        """get last sent message

        :return: object of last sent message
        :rtype: QueueMessage
        """
        return self.last_sent_message

    def retrieve_messages(self):
        """read and retrieve messages
        - messages are invisible for others during 30s
        - messages are assumed to be deleted with delete method in 30s delay
        - after 30s, messages become visible for thers

        :return: Iterator on messages in queue
        :rtype: List[QueueMessage]
        """
        return self.client.receive_messages()

    def read_messages(self):
        """read message without retrieving

        :return: Iterator on messages in queue
        :rtype: List[QueueMessage]
        """
        return self.client.peek_messages()

    def delete_message(self, message: QueueMessage):
        """delete message

        :param message: message object retrieved by retrive_messages method
        (it will not work with message objects returned by read_messages method)
        :type message: QueueMessage
        :return: self
        :rtype: Queue
        """
        self.client.delete_message(message)
        return self
