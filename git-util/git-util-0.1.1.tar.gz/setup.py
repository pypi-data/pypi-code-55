# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_util']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.51,<2.0',
 'click>=7.1.2,<8.0.0',
 'gitpython>=3.1.2,<4.0.0',
 'pobject>=0.1.5,<0.2.0',
 'url-util>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['git-util = git_util.cli:cli']}

setup_kwargs = {
    'name': 'git-util',
    'version': '0.1.1',
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
