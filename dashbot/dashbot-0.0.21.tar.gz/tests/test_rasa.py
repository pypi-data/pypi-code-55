import os
from rasa.core.brokers.broker import EventBroker
from rasa.utils.endpoints import read_endpoint_config
from dashbot.rasa import rasa


def test_dashbot_config():
    cfg = read_endpoint_config(
        os.path.join(os.path.dirname(__file__), "data/rasa_endpoints.yml"), "event_broker"
    )
    actual = EventBroker.create(cfg)

    assert isinstance(actual, rasa)
    assert actual.proxies['http'] == 'http://10.10.1.10:3128'
    assert actual.proxies['https'] == 'http://10.10.1.10:1080'
    assert actual.apiKey == 'here'
