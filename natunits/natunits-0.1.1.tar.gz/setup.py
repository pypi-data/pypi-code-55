# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['natunits']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'natunits',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Hajime Fukuda',
    'author_email': 'hajime.fukuda@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
