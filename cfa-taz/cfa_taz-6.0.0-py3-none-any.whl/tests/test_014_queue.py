#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from taz.storage_account import StorageAccount
from taz.queue import Queue
from tests.decorator import waitingdots

import tests.config


storage_account = None
queue = None


@waitingdots
def test_010_storage_account_connection():
    global storage_account
    storage_account = StorageAccount(
        connection_string=tests.config.queue["storage_connection_string"]
    )


@waitingdots
def test_020_list_queues():
    global storage_account
    for queue in storage_account.list_queues():
        print(queue)


@waitingdots
def test_030_queue_create():
    global queue
    queue = Queue(tests.config.queue["queue_name"], storage_account)
    queue.create()


@waitingdots
def test_040_send_message():
    global queue
    queue.send('{"body": "test message"}')


@waitingdots
def test_050_read_messages():
    global queue
    for message in queue.read_messages():
        print(message)


@waitingdots
def test_060_retrieve_messages():
    global queue
    for message in queue.retrieve_messages():
        print(message)
        queue.delete_message(message)


@waitingdots
def test_070_delete_queue():
    global queue
    queue.delete()
