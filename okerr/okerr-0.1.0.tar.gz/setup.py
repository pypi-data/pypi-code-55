# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okerr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'okerr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rafael Marques',
    'author_email': 'rafaelomarques@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
