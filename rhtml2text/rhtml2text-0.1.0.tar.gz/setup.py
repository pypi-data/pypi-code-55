# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhtml2text']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rhtml2text',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'scottming',
    'author_email': 'therealscottming@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
