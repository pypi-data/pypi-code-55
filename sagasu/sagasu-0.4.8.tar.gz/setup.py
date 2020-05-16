# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sagasu']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ginza>=3.1.2,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pillow>=7.1.2,<8.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'spacy>=2.2.4,<3.0.0',
 'tqdm>=4.46.0,<5.0.0',
 'tweepy>=3.8.0,<4.0.0']

entry_points = \
{'console_scripts': ['sagasu = sagasu.app:app']}

setup_kwargs = {
    'name': 'sagasu',
    'version': '0.4.8',
    'description': 'sagasu is search all my contents',
    'long_description': None,
    'author': 'funwarioisii',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
