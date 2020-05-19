# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasa_integration_testing']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'click>=7.1.1,<8.0.0',
 'coloredlogs>=10.0,<11.0',
 'jinja2>=2.11.2,<3.0.0',
 'ruamel-yaml>=0.16.10,<0.17.0']

setup_kwargs = {
    'name': 'rasa-integration-testing',
    'version': '0.1.3',
    'description': 'A tool for end-to-end testing Rasa bots',
    'long_description': None,
    'author': 'Nu Echo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
