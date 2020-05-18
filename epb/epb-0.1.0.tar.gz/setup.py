# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'epb',
    'version': '0.1.0',
    'description': 'Energy performance of buildings',
    'long_description': '# Energy performance of buildings\n\nThis library provides helpers for energy performance of buildings computation.\n',
    'author': 'Arthur White',
    'author_email': 'arthur@white.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/immoveable/epb-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
