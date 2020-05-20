# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['injector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'document-variable-injector',
    'version': '0.1.0',
    'description': 'Provides method for dynamically injecting variables into a document and/or HTML like object',
    'long_description': None,
    'author': 'Alex Pedersen',
    'author_email': 'me@alexpdr.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
