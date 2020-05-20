# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uncompressor']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['uncmprs = uncompressor.main:main']}

setup_kwargs = {
    'name': 'uncompressor',
    'version': '0.1.0',
    'description': 'easy file uncompressor.',
    'long_description': None,
    'author': 'Hibiki Okada',
    'author_email': '4617016@ed.tus.ac.jp',
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
