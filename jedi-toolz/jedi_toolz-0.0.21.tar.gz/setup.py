# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jedi_toolz']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=4.4.2,<5.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pydomo>=0.2.3,<0.3.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jedi-toolz',
    'version': '0.0.21',
    'description': 'A collection of utilities to simplify a data workflow using pandas, Excel, DOMO, and other tools.',
    'long_description': None,
    'author': 'JediHero',
    'author_email': 'hansen.rusty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JediHero/jedi_toolz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
