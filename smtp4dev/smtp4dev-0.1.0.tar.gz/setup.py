# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smtp4dev']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'smtp4dev',
    'version': '0.1.0',
    'description': 'Provides access to emails caught by the SMTP4dev development server',
    'long_description': None,
    'author': 'Guillaume Pasquet',
    'author_email': 'guillaume.pasquet@plentific.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
