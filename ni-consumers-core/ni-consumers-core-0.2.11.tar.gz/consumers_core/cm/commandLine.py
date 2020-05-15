import click
import coloredlogs

from ..consumer import ReconnectingExampleConsumer
from .main import load_consumer_file, find_consumer_file


@click.command(name='consumer')
@click.option('--file', '-f', default='consumer.py', required=True, help='Consumer file action')
@click.option('--log-level', '-l', default='INFO', help='Log level')
@click.option('--amqp-username', '-u', default='guest', help='AMQP Username')
@click.option('--amqp-password', '-p', default='guest', help='AMQP Password')
@click.option('--amqp-url', '-r', default='localhost', help='AMQP url')
@click.option('--amqp-port', '-P', default=5672, help='AMQP port')
@click.option('--core-url', '-c', default='http://localhost:8888', help='Core server url')
@click.option('--queue-name', '-q', required=True, help='queue name to observe')
def cm(file, log_level, amqp_username, amqp_password, amqp_url, amqp_port, core_url, queue_name):
    coloredlogs.install(level=log_level)
    amqp_url = f'amqp://{amqp_username}:{amqp_password}@{amqp_url}:{amqp_port}/%2F'

    # Load implementation
    consumer_file = find_consumer_file(file)
    _,action_class = load_consumer_file(consumer_file)

    # Launch consumer
    # @Fixme Revoir cette partie pour la découverte de la classe action!
    consumer = ReconnectingExampleConsumer(amqp_url, queue_name, core_url, action_class[list(action_class.keys())[1]]())
    consumer.run()
