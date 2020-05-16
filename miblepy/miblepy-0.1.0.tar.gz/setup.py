# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miblepy', 'miblepy.devices', 'miblepy.devices.xbm']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3,<2.0',
 'btlewrap>=0.0.8,<0.0.9',
 'click>=7.1.2,<8.0.0',
 'miflora>=0.6,<0.7',
 'paho-mqtt>=1.5.0,<2.0.0',
 'tomlkit>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['miblepy = miblepy.cli:cli']}

setup_kwargs = {
    'name': 'miblepy',
    'version': '0.1.0',
    'description': 'miblepy fetches data from various (Xiaomi/Mijia/Mi) Bluetooth LE devices and push it to a MQTT broker in a coordinated, sequential manner.',
    'long_description': None,
    'author': 'Ben Lebherz',
    'author_email': 'git@benleb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
