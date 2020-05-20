# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'inutils',
    'version': '0.1.3',
    'description': 'INternational UTILS - random utilities',
    'long_description': None,
    'author': 'Luiz Menezes',
    'author_email': 'luiz.menezesf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
