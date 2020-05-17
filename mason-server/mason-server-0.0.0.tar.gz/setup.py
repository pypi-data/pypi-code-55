# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mason_server']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6.0,<2.0.0', 'mason-framework>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'mason-server',
    'version': '0.0.0',
    'description': 'Backend server for mason framework.',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
