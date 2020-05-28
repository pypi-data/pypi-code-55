""" logging to rabbitmq then file """
import os
from threading import Thread
from pipemaker.qrabbit import pika
import pickle
from logging.handlers import QueueHandler
import logging

# used by handler and stream
qdef = dict(queue="Logq", auto_delete=True)


class SharedQueueHandler(QueueHandler):
    """ handler that puts log messages on rabbitmq """

    def __init__(self, ch=None):
        """
        :param ch: ch to publish messages. None creates new ch
        """
        self.ch = ch
        self.q = self.ch.queue_declare(**qdef)
        super().__init__(self.q)

    def enqueue(self, record):
        """ log the record """
        self.ch.basic_publish(
            body=pickle.dumps(record), exchange="", routing_key=self.q.method.queue
        )


class FileHandler(logging.FileHandler):
    """ read messages from the rabbit log queue (qdef above) and write to file """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log = logging.getLogger()
        if log.handlers:
            self.setFormatter(log.handlers[0].formatter)
        self.start()

    def start(self):
        """ background thread to consume messages """

        def target():
            ch = pika.get_channel(client_properties=dict(connection_name="logq"))
            q = ch.queue_declare(**qdef)
            ch.basic_consume(queue=q.method.queue, on_message_callback=self.callback)
            ch.start_consuming()
            ch.connection.close()

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def callback(self, ch, method, properties, body):
        self.emit(pickle.loads(body))
        ch.basic_ack(method.delivery_tag)
