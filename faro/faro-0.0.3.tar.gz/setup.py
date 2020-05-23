# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faro']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0', 'pydantic>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'faro',
    'version': '0.0.3',
    'description': 'An SQL-focused data analysis library for Python',
    'long_description': None,
    'author': 'Yannis Katsaros',
    'author_email': 'yanniskatsaros@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
