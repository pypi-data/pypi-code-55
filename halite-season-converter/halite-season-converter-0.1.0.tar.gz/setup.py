# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['halite_season_converter',
 'halite_season_converter.converters',
 'halite_season_converter.schemas']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.4.2,<0.5.0',
 'kaggle-environments>=0.2.6,<0.3.0',
 'requests>=2.23.0,<3.0.0',
 'zstd>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'halite-season-converter',
    'version': '0.1.0',
    'description': 'Bidirectional converter for Halite season 2, 3 and 3.1.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
