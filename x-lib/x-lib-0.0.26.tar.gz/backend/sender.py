import ssl

from kafka import KafkaProducer
from backend.encoder import JsonEncoder
import json
import os

context = ssl.create_default_context()
context.options &= ssl.OP_NO_TLSv1
context.options &= ssl.OP_NO_TLSv1_1


def send_message(topic, input_dict, partition=0):
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_SERVER'),
        sasl_mechanism='PLAIN',
        security_protocol='SASL_SSL',
        ssl_context=context,
        sasl_plain_username=os.getenv('KAFKA_USERNAME'),
        sasl_plain_password=os.getenv('KAFKA_PASSWORD'),
        value_serializer=lambda v: json.dumps(v, cls=JsonEncoder).encode('utf-8'),
    )
    if partition > 0:
        future = producer.send(topic, input_dict, partition=partition)
    else:
        future = producer.send(topic, input_dict)
    future.get(timeout=int(os.getenv('KAFKA_TIME_OUT')))
