# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['race']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>0.1']}

setup_kwargs = {
    'name': 'race',
    'version': '0.0.1',
    'description': '',
    'long_description': 'race\n====\n\nRace condition modelling package.\n\n',
    'author': 'Andrey Cizov',
    'author_email': 'acizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreycizov/python-race',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
