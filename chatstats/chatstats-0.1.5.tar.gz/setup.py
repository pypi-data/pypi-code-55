# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatstats']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'chatstats',
    'version': '0.1.5',
    'description': 'python sdk for chat-stats.ru',
    'long_description': None,
    'author': 'Bogdan',
    'author_email': 'evstrat.bg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
