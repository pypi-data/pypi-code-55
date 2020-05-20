# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_streamer']

package_data = \
{'': ['*']}

install_requires = \
['avro-schema>=0.1.1,<0.2.0',
 'confluent_avro>=1.7.0,<2.0.0',
 'confluent_kafka>=1.4.1,<2.0.0',
 'fastavro>=0.23.3,<0.24.0',
 'pydantic>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'kafka-streamer',
    'version': '0.2.1',
    'description': '',
    'long_description': '# kafka-streamer\nApache Kafka python client for streaming data\n',
    'author': 'Sam Mosleh',
    'author_email': 'sam.mosleh@ut.ac.ir',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sam-mosleh/kafka-streamer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
