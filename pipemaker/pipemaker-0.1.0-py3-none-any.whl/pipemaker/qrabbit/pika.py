import pika
import pipemaker.master as m
from ..utils import dotdict
import logging

log = logging.getLogger(__name__)


def get_channel(**params):
    """ return a new rabbit ch on new connection. this is used by consumers and producers
    :param params: additional parameters for connection

    rabbitmq recommendation is one connection per process; one ch per thread; both split producer/consumer
    however sharing channels between threads does not work in pika (nor other clients)
    """
    c = m.CREDS[m.CONFIG.server]
    params.update(
        host=c.host,
        credentials=pika.PlainCredentials(c.user, c.password),
        virtual_host=c.vhost,
        socket_timeout=5,
    )
    params = pika.connection.ConnectionParameters(**params)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return channel
