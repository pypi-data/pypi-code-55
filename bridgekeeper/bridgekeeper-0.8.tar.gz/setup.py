# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bridgekeeper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bridgekeeper',
    'version': '0.8',
    'description': 'Django permissions that work with QuerySets.',
    'long_description': None,
    'author': 'Leigh Brenecki',
    'author_email': 'leigh@brenecki.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bridgekeeper.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
