# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dkpf']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'cleo>=0.8.0,<0.9.0',
 'flake8>=3.7.9,<4.0.0',
 'loguru>=0.4.1,<0.5.0',
 'tomlkit>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['dkpf = dkpf.cli:main']}

setup_kwargs = {
    'name': 'digikam-photo-finder',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@pm.me',
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
