from mq_http_sdk.mq_exception import MQExceptionBase
from mq_http_sdk.mq_producer import TopicMessage
from mq_http_sdk.mq_client import MQClient
import logging
import json
import contextlib
import functools


__mq_client = None


def _get_mq_client(http_endpoint, access_key, secret_key):
    global __mq_client
    if __mq_client is None:
        __mq_client = MQClient(http_endpoint, access_key, secret_key)
        return __mq_client
    else:
        return __mq_client


class Client(object):
    def __init__(self, http_endpoint, access_key, secret_key):
        self.mq_client = _get_mq_client(http_endpoint, access_key, secret_key)

    @classmethod
    def get_client_from_config(cls, config_host, config_username, config_password, config_application, config_profile,
                               http_endpoint_config='base.comm.rocket-mq.onsAddr.digital.http',
                               access_key_config='base.rocket-mq.accessKeyId',
                               secret_key_config='base.rocket-mq.accessKeySecret'):
        from doubao_config import Client as ConfigClient
        config_client = ConfigClient(config_host, config_username, config_password)
        config = config_client.get_config(config_application, config_profile)
        return cls(config[http_endpoint_config], config[access_key_config], config[secret_key_config])

    def get_producer(self, instance_id, topic_name):
        return Producer(self.mq_client, instance_id, topic_name)

    def get_consumer(self, instance_id, topic_name, group_id):
        return Consumer(self.mq_client, instance_id, topic_name, group_id)


class Producer:
    def __init__(self, mq_client, instance_id, topic_name):
        self.producer = mq_client.get_producer(instance_id, topic_name)

    def send(self, msg, tag='', properties=None, key=None, start_deliver_time=None):
        _properties = properties if properties else {}
        for _ in range(3):
            try:
                msg = TopicMessage(message_body=msg, message_tag=tag)
                for k, v in _properties:
                    msg.put_property(k, v)
                if key is not None:
                    msg.set_message_key(key)
                if start_deliver_time:
                    msg.set_start_deliver_time(start_deliver_time)
                re_msg = self.producer.publish_message(msg)
                logging.info("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (re_msg.message_id, re_msg.message_body_md5))
                return re_msg
            except MQExceptionBase as e:
                if e.type in ['TopicNotExist', 'AccessDenied']:
                    raise e
                logging.error("Publish Message Fail. Exception:%s" % e)
                continue
            except Exception as e:
                raise e

    def send_json(self, json_msg, tag='', properties=None, key=None, start_deliver_time=None):
        return self.send(json.dumps(json_msg), tag=tag, properties=properties, key=key, start_deliver_time=start_deliver_time)


class Consumer:
    def __init__(self, mq_client, instance_id, topic_name, group_id):
        self.consumer = mq_client.get_consumer(instance_id, topic_name, group_id)

    def receive(self, batch=1, wait_seconds=3):
        try:
            recv_msgs = self.consumer.consume_message(batch, wait_seconds)
            return recv_msgs
        except MQExceptionBase as e:
            if e.type != "MessageNotExist":
                raise e

    def ack_message(self, recv_msgs):
        if recv_msgs:
            try:
                receipt_handle_list = [msg.receipt_handle for msg in recv_msgs]
                self.consumer.ack_message(receipt_handle_list)
            except MQExceptionBase as e:
                logging.error("Ak Message Fail! Exception: %s" % e)

    @contextlib.contextmanager
    def consume(self, batch=1, wait_seconds=3):
        recv_msgs = self.receive(batch=batch, wait_seconds=wait_seconds)
        if recv_msgs is None:
            recv_msgs = []
        yield recv_msgs
        self.ack_message(recv_msgs)

    def consume_decorator(self, batch=1, wait_seconds=3):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.consume(batch=batch, wait_seconds=wait_seconds) as recv_msgs:
                    out = func(recv_msgs, *args, **kwargs)
                return out
            return wrapper
        return decorator
