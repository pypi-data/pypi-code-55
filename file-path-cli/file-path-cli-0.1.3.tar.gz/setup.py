# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_path_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyperclip>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['file-path-cli = file_path_cli.cli:cli']}

setup_kwargs = {
    'name': 'file-path-cli',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
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
