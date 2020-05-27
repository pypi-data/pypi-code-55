# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keios_zmq', 'keios_zmq.serialization']

package_data = \
{'': ['*']}

install_requires = \
['aiozmq>=0.7.1,<0.8.0', 'pyzmq>=18.0,<19.0']

entry_points = \
{'console_scripts': ['build = poetry_scripts:build',
                     'install = poetry_scripts:install',
                     'publish = poetry_scripts:publish',
                     'release = poetry_scripts:release',
                     'test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'keios-zmq',
    'version': '1.3.2',
    'description': '',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': 'contact@leftshift.one',
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
