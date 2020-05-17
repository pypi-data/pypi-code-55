# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tracers', 'tracers.function']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tracers',
    'version': '20.5.23346',
    'description': 'Decorator-like performance tracing tool',
    'long_description': '',
    'author': 'Kevin Amado',
    'author_email': 'kamadorueda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamadorueda/tracers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
