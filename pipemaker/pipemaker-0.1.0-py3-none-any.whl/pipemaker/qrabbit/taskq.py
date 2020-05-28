from . import pika
from threading import Thread
import pickle
import logging

log = logging.getLogger(__name__)

qdef = dict(queue="Taskq", auto_delete=True)


class Taskq:
    """ Consumer for rabbitmq event queue """

    name = "Taskq"

    def __init__(self, taskdb):
        self.taskdb = taskdb
        self.start()

    @classmethod
    def start_server(cls):
        pass

    def start(self):
        """ background thread to consume messages """

        def target():
            try:
                ch = pika.get_channel(client_properties=dict(connection_name="taskq"))
                ch.queue_declare(**qdef)
                ch.basic_consume(queue=self.name, on_message_callback=self.callback)
                ch.start_consuming()
                ch.connection.close()
            except:
                log.exception("Error in taskq consumer")

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def callback(self, ch, method, properties, body):
        """ callback when message received """
        try:
            body = pickle.loads(body)
            getattr(self.taskdb, body["event"])(body)
        except:
            log.exception(f"Error processing event {body}")
        finally:
            ch.basic_ack(method.delivery_tag)

    def stop(self):
        self.taskdb.clear()


class TaskqP:
    """ Producer for rabbitmq event queue """

    def __init__(self, ch=None):
        self.name = "Taskq"
        ch.queue_declare(**qdef)
        self.ch = ch

    def put(self, body=""):
        """ put a message on the queue
        :param body: message to send
        """
        body = pickle.dumps(body)
        self.ch.basic_publish(exchange="", routing_key=self.name, body=body)
