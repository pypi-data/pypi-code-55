#!/usr/bin/env python
import pickle
from threading import Thread
import functools
import multiprocessing as mp
import pipemaker.master as m
from pipemaker.qrabbit import pika
import logging

log = logging.getLogger(__name__)

qdef = dict(queue="Workerq", auto_delete=True)


class Workerq:
    """ a task queue that executes one task at a time in a thread """

    @classmethod
    def start_server(cls):
        pass

    @classmethod
    def consumers(cls, ch, **kwargs):
        return ch.queue_declare(**qdef).method.consumer_count

    def process_target(self):
        try:
            # consumer
            ch = pika.get_channel(
                client_properties=dict(
                    connection_name=f"workerq {mp.current_process().name}"
                )
            )
            ch.queue_declare(**qdef)
            ch.basic_qos(prefetch_count=1)
            ch.basic_consume(queue="Workerq", on_message_callback=self.callback)
            ch.start_consuming()
            ch.connection.close()
        except:
            log.exception("Error in worker")

    def start(self, name=""):
        """ create background process as workers need to utlise cpus
        :return: process so it can be deleted in exit
        """
        self.p = mp.Process(target=self.process_target, daemon=True, name=name)
        self.p.start()

    def callback(self, ch, method, properties, body):
        """ callback when message received """

        def target():
            body2 = pickle.loads(body)
            try:
                from ..utils import defaultlog
                import pipemaker.master as m

                # taskqP and logqP share same connection
                chP = pika.get_channel(
                    client_properties=dict(
                        connection_name=f"worker {mp.current_process().name}"
                    )
                )
                rootlog = logging.getLogger()
                rootlog.addHandler(m.loghandler.SharedQueueHandler(ch=ch))

                body2.taskqP = m.TaskqP(ch=chP.connection.channel())
                body2.run()
            except:
                log.exception(f"Unable to handle message={body2}")
            finally:
                cb = functools.partial(ch.basic_ack, method.delivery_tag)
                ch.connection.add_callback_threadsafe(cb)
                chP.connection.close()

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def stop(self):
        """ stops cleanly when connections closed """
        pass


class WorkerqP:
    """ default exchange with routing to class name  """

    def __init__(self, ch=None):
        """
        :param ch: pika ch passed as parameter as can be shared by multiple queues in the same thread
        """
        self.name = self.__class__.__name__
        self.ch = ch
        ch.queue_declare(**qdef)

    def put(self, body=""):
        """ put a message on the queue
        :param body: message to send
        """
        body = pickle.dumps(body)
        self.ch.basic_publish(exchange="", routing_key="Workerq", body=body)
