# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poethepoet', 'poethepoet.cli']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['poe = poethepoet.cli:main']}

setup_kwargs = {
    'name': 'poethepoet',
    'version': '0.0.1',
    'description': 'A task runner that works well with poetry.',
    'long_description': None,
    'author': 'Nat Noordanus',
    'author_email': 'n@natn.me',
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
