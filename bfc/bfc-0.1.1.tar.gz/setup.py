# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bfc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bfc',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'bfconsidine',
    'author_email': 'ben@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
