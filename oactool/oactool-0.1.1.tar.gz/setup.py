# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oactool', 'oactool.renderers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'jsonref>=0.2,<0.3',
 'more-itertools>=8.3.0,<9.0.0',
 'pydantic>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['oactool = oactool.main:main']}

setup_kwargs = {
    'name': 'oactool',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Alexander Shishenko',
    'author_email': 'alex@shishenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openautocomplete/oactool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
