# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['env_resolver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'env-resolver',
    'version': '0.1.0',
    'description': 'A utility for resolving ssm parameters and secretsmanager secrets',
    'long_description': None,
    'author': 'Joe Snell',
    'author_email': 'joepsnell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
