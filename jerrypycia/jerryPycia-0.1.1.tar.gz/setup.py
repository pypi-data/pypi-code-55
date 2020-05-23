# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jerrypycia']

package_data = \
{'': ['*'], 'jerrypycia': ['datasets/*']}

install_requires = \
['matplotlib>=3.2,<4.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'jerrypycia',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Andrew Blance',
    'author_email': 'andrewblance@live.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
