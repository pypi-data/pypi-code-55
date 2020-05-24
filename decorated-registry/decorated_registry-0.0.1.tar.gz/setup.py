# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decorated_registry']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>0.1']}

setup_kwargs = {
    'name': 'decorated-registry',
    'version': '0.0.1',
    'description': '',
    'long_description': 'decorated_registry\n==================\n\nImplementation of generalised registries for Python.\n\n\n',
    'author': 'Andrey Cizov',
    'author_email': 'acizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreycizov/python-decorated_registry',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
