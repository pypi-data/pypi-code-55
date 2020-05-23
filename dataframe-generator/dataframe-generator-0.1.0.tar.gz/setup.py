# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataframe_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataframe-generator',
    'version': '0.1.0',
    'description': 'A simple Python module for generating test CSV datasets from PySpark schemas.',
    'long_description': None,
    'author': 'Szabolcs Vasas',
    'author_email': 'vasas@apache.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
