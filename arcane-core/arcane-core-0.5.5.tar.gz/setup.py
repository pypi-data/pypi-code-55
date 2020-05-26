# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.core']

package_data = \
{'': ['*']}

install_requires = \
['arcane-firebase==0.1.2', 'backoff>=1.10.0,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'arcane-core',
    'version': '0.5.5',
    'description': 'Common utility functions',
    'long_description': None,
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
