from .utils import encode_bson, decode_bson
from pika.exceptions import ProbableAccessDeniedError, ConnectionClosedByBroker
from re import match
import pika
import logging
import requests
import json
import uuid
import copy
import sys

LOGGER = logging.getLogger()  # root logger
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(stream_handler)


class CreateVhostException(Exception):
    pass


class CreatePermissionException(Exception):
    pass


class RabbitmqManagement(object):
    MANAGEMENT_PORT = 15672
    """
        Rabbitmq management api requests
    """

    def __init__(self, host, username, password):
        self.username = username
        self.password = password
        self.host = host
        self.uri = "http://%s:%s" % (self.host, self.MANAGEMENT_PORT)

    def request_with_credentials(self, url, method="get", data=None):
        req = getattr(requests, method)
        response = req(
            url,
            headers={"content-type": "application/json"},
            data=data,
            auth=(self.username, self.password)
        )
        response.raise_for_status()
        return json.loads(response.content)

    @property
    def messages(self):
        url = "%s/api/queues/" % self.uri
        res = self.request_with_credentials(url)
        return res

    def create_vhost(self, vhost):
        url = "%s/api/vhosts/%s" % (self.uri, vhost)
        try:
            self.request_with_credentials(url, method="put")
        except Exception:
            raise CreateVhostException("Attempt to create temporary vhost=%s failed. url=%r" % (vhost, url))

    def create_permission(self, vhost):
        url = "%s/api/permissions/%s/%s" % (self.uri, vhost, self.username)
        try:
            self.request_with_credentials(url, method="put",
                                          data=json.dumps({"configure": ".*", "write": ".*", "read": ".*"}))
        except Exception:
            raise CreatePermissionException("Attempt to configure premissions on vhost=%s failed. url=%r"
                                            % (vhost, url))

    @classmethod
    def create_vhost_and_permission(cls, vhost, *args, **kwargs):
        klass = cls(*args, **kwargs)
        klass.create_vhost(vhost=vhost)
        klass.create_permission(vhost=vhost)


class Queue(object):
    def __init__(self, uri, vhost, queue_name="", routing_key="", exchange="", exchange_type='fanout',
                 exchange_durable=True, queue_durable=True):
        uri = uri.replace('<vhost>', vhost)
        self.uri = uri
        self.exchange = exchange
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.exchange_type = exchange_type
        self.exchange_durable = exchange_durable
        self.queue_durable = queue_durable
        self.connection, self.channel = self.connect(uri)

    def close(self):
        self.connection.close()
        self.channel.close()

    @classmethod
    def connect(cls, uri):
        """
        :param uri: amqp://guest:guest@rabbitmq.marathon.mesos:5672/vhost?socket_timeout=10
        :return: connection, channel
        """
        LOGGER.info('Connection to %s', uri)
        params = pika.URLParameters(uri)
        try:
            connection = pika.BlockingConnection(params)
        except (ProbableAccessDeniedError, ConnectionClosedByBroker) as e:
            try:
                code, message = e
            except TypeError:
                code, message = e.args
            if match('NOT_ALLOWED - vhost \S+ not found', message):
                RabbitmqManagement.create_vhost_and_permission(params.virtual_host, params.host,
                                                               params.credentials.username, params.credentials.password)
            connection = pika.BlockingConnection(params)
        channel = connection.channel()
        return connection, channel

    def configure(self):
        """ Declare exchange and queue then queue bind to exchange
        :return:
        """
        self.exchange_declare()
        self.queue_declare()
        self.queue_bind()

    def queue_declare(self, exclusive=False):
        return self.channel.queue_declare(queue=self.queue_name, durable=self.queue_durable, exclusive=exclusive)

    def exchange_declare(self):
        return self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type,
                                             durable=self.exchange_durable)

    def queue_bind(self):
        return self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange)

    def publish(self, body, properties=None):
        prop_dict = copy.deepcopy(properties)
        if properties:
            properties = pika.BasicProperties(**properties)
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue_name, body=body,
                                       properties=properties)
        except Exception as cex:
            LOGGER.info('Exception=%s , Re-configuring the publisher' % cex)
            self.connection, self.channel = self.connect(self.uri)
            self.configure()
            self.publish(body, prop_dict)

    def get_message(self):
        method, properties, body = self.channel.basic_get(self.queue_name, auto_ack=True)
        return method, properties, decode_bson(body)


class BaseConsumer(object):
    def __init__(self, queue):
        self.q = queue
        self.channel = queue.channel
        self.connection = queue.connection
        self.queue_name = queue.queue_name
        self.callback_func = lambda ch, method, properties, body: self.process(ch, method, properties,
                                                                               decode_bson(body))

    def start_consuming(self, prefetch_count=1):
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(self.queue_name, self.callback_func)
        self.channel.start_consuming()

    def process(self, ch, method, properties, body):
        """ Callback function
        :param body:
        :return:
        """
        raise NotImplementedError()

    def close(self):
        try:
            self.channel.close()
            self.connection.close()
        except Exception as e:
            LOGGER.info(e)
            pass

    def start(self):
        """ basic_consume and start_consuming operations
        :return:
        """
        while True:
            _reconfigure = False
            try:
                self.start_consuming()
                LOGGER.info('Consuming started.')
            except pika.exceptions.StreamLostError as stream_lost_error:
                LOGGER.info(stream_lost_error)
                _reconfigure = True
            except pika.exceptions.ChannelWrongStateError as channel_wrong_state_error:
                LOGGER.info(channel_wrong_state_error)
                _reconfigure = True
            except pika.exceptions.ConnectionClosedByBroker as connection_closed_by_broker:
                LOGGER.info(connection_closed_by_broker)
                _reconfigure = True
            except pika.exceptions.AMQPChannelError as err:
                LOGGER.info("Caught a channel error: {}, stopping...".format(err))
                break
            except pika.exceptions.AMQPConnectionError:
                LOGGER.info("Connection was closed, retrying...")
                _reconfigure = True
            except Exception as e:
                LOGGER.info(e)
                _reconfigure = True

            if _reconfigure:
                self.close()
                self.reconfigure_queue()
                _reconfigure = False

    def get_and_publish(self):
        """ Consume one message and close connection
        :return:
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.queue_name, self.callback_func, auto_ack=True)
        self.connection.process_data_events(time_limit=None)
        self.connection.close()

    def reconfigure_queue(self):
        LOGGER.info('#### Reconfiguring queue ####')
        conn, channel = self.q.connect(self.q.uri)
        self.q.connection = conn
        self.q.channel = channel
        self.connection = conn
        self.channel = channel
        self.q.configure()

    def stop(self):
        self.channel.stop_consuming()
        LOGGER.info('Consuming stopped.')


class RpcClient(object):
    def __init__(self, uri, vhost, publish_to):
        """
        Rpc server is match with "options.wait_response" flag in body, publish the response to callback_queue
        """
        self.queue = Queue(uri, vhost)
        self.publish_to = publish_to
        self.callback_queue = self.queue.queue_declare(durable=False, exclusive=True).method.queue
        self.queue.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def publish_and_wait(self, body, wait_response=True, continue_pipe=True):
        body['options'] = {
            "wait_response": wait_response,
            "continue_pipe": continue_pipe
        }
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.queue.channel.basic_publish(
            exchange='',
            routing_key=self.publish_to,
            body=encode_bson(body),
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id)
        )
        while self.response is None:
            self.queue.connection.process_data_events()
        return self.response


class QueueStats(object):

    def __init__(self, url, user, password, vhost, queue_name, age=600):
        self.url = url
        self.user = user
        self.password = password
        self.vhost = vhost
        self.queue_name = queue_name
        self.age = age
        self.stats = self.get_stats()

    def get_stats(self):
        url = '/'.join([self.url, 'api', 'queues', self.vhost, self.queue_name])
        url += '?lengths_age={secs}&lengths_incr=5&msg_rates_age={secs}&msg_rates_incr=5'.format(secs=self.age)
        queue_info = requests.get(url, auth=(self.user, self.password))
        if queue_info.status_code != 200:
            LOGGER.warn("Rabbitmq api response is not 200, Url: %s,  Status: %s, Reason: %s", url,
                        queue_info.status_code, queue_info.reason)
        return json.loads(queue_info.content)

    @property
    def message_count(self):
        return self.stats.get('messages', 0)

    @property
    def ack_rate(self):
        return self.stats.get('message_stats', {}).get('ack_details', {}).get('rate', 0)

    @property
    def publish_rate(self):
        return self.stats.get('message_stats', {}).get('publish_details', {}).get('rate', 0)

    @property
    def deliver_rate(self):
        return self.stats.get('message_stats', {}).get('deliver_details', {}).get('rate', 0)

    @property
    def ack_avg_rate(self):
        return self.stats.get('message_stats', {}).get('ack_details', {}).get('avg_rate', 0)

    @property
    def publish_avg_rate(self):
        return self.stats.get('message_stats', {}).get('publish_details', {}).get('avg_rate', 0)

    @property
    def deliver_avg_rate(self):
        return self.stats.get('message_stats', {}).get('deliver_details', {}).get('avg_rate', 0)

    @classmethod
    def queues_stats(cls, url, user, password, vhost):
        """
            take knowledge queues under the vhost
        :param url:
        :param user:
        :param password:
        :param vhost:
        :return:
        """
        url_all_queues = '/'.join([url, 'api', 'queues', vhost])
        queue_info = requests.get(url_all_queues, auth=(user, password))
        if queue_info.status_code != 200:
            raise Exception('sdsd')
        a = json.loads(queue_info.content)
        queue_names = set()
        for i in a:
            queue_names.add(i['name'])


        message_rates = dict(queues=dict())

        message_count, total_publish_avg_rate, total_ack_avg_rate = 0, 0, 0
        for queue_name in queue_names:
            c = cls(url, user, password, vhost, queue_name=queue_name)
            message_rates['queues'][queue_name] = {
                'message_count': c.message_count,
                "publish_avg_rate": c.publish_avg_rate,
                "deliver_avg_rate": c.deliver_avg_rate,
                "ack_avg_rate": c.ack_avg_rate,
                "publish_rate": c.publish_rate,
                "deliver_rate": c.deliver_rate,
                "ack_rate": c.ack_rate
            }
            message_count += c.message_count
            total_publish_avg_rate += c.publish_avg_rate
            total_ack_avg_rate += c.ack_avg_rate
            if c.message_count and not c.ack_avg_rate:
                LOGGER.warn('Wait <%s> messages in <%s> queue but not consume.', c.message_count, queue_name)
        message_rates['total_message_count'] = message_count
        message_rates['total_publish_avg_rate'] = total_publish_avg_rate
        message_rates['total_ack_avg_rate'] = total_ack_avg_rate
        return message_rates
