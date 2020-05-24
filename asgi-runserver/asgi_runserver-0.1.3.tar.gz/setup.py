# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_runserver',
 'asgi_runserver.management',
 'asgi_runserver.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['daphne>=2.5.0,<3.0.0', 'django>=3.0.6,<4.0.0']

setup_kwargs = {
    'name': 'asgi-runserver',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Joshua Massover',
    'author_email': 'massover@simplebet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
