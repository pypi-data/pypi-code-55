# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mark_sideways']

package_data = \
{'': ['*']}

install_requires = \
['rich>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['mark = mark_sideways.cli:mark']}

setup_kwargs = {
    'name': 'mark-sideways',
    'version': '0.1.0',
    'description': 'Render markdown in the terminal',
    'long_description': None,
    'author': 'chris48s',
    'author_email': None,
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
