# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photocrawl']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0',
 'loguru>=0.4.1,<0.5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyexifinfo>=0.4.0,<0.5.0',
 'seaborn>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'photocrawl',
    'version': '0.2.0',
    'description': 'Analysis script of photography habits.',
    'long_description': None,
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
