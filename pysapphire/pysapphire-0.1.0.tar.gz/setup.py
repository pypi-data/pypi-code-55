# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysapphire']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysapphire',
    'version': '0.1.0',
    'description': 'Python implementation of the Sapphire II Stream Cipher Algorithm',
    'long_description': None,
    'author': 'Jasper Chan',
    'author_email': 'jasperchan515@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
