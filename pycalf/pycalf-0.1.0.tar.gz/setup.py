# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycalf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycalf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'konumaru',
    'author_email': 'konumaru1022@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
