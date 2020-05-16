# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factpy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['run-factpy = factpy.__main__:run']}

setup_kwargs = {
    'name': 'factpy',
    'version': '0.1.0',
    'description': 'Calculator for the game Factorio',
    'long_description': None,
    'author': 'Jels Boulangier',
    'author_email': 'boulangier.jels@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
