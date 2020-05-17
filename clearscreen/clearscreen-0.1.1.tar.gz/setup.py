# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearscreen', 'clearscreen.art']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['cls = clearscreen.cli:main']}

setup_kwargs = {
    'name': 'clearscreen',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Tim Simpson',
    'author_email': 'timsimpson4@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
