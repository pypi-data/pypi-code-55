# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clint', 'clint.packages', 'clint.packages.colorama', 'clint.textui']

package_data = \
{'': ['*']}

modules = \
['functions', 'core', 'readme']
entry_points = \
{'console_scripts': ['gossip = core:app']}

setup_kwargs = {
    'name': 'dev-gossip',
    'version': '0.2.5',
    'description': '',
    'long_description': None,
    'author': 'shols232',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
