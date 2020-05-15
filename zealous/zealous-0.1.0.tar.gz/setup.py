# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zealous']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zealous',
    'version': '0.1.0',
    'description': 'Zealous Framework',
    'long_description': None,
    'author': 'Jonathan Gravel',
    'author_email': 'un@stashed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
