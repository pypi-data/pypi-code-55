# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_repo_walker']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['repo-walker = examples.cli:main']}

setup_kwargs = {
    'name': 'git-repo-walker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Elsner',
    'author_email': 'daniel.elsner@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
