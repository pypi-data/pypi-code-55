# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_sage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-sage',
    'version': '0.1.0a0',
    'description': 'Security Headers for asgi apps',
    'long_description': None,
    'author': 'Jt Miclat',
    'author_email': 'jtmiclat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
