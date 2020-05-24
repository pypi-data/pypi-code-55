# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sudoisbot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'loguru>=0.5.0,<0.6.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'python-telegram-bot',
 'requests>=2.23.0,<3.0.0',
 'zmq>=0.0.0,<0.0.1']

entry_points = \
{'console_scripts': ['proxy_pubsub = proxy.proxy_pubsub:main',
                     'sendtelegram = sudoisbot.sendtelegram:main',
                     'temper_sub = temps.temper_sub:main',
                     'tglistener = sudoisbot.tglistener:main',
                     'unifi_clients = unifi.unifi:show_clients']}

setup_kwargs = {
    'name': 'sudoisbot',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Benedikt Kristinsson',
    'author_email': 'benedikt@lokun.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
