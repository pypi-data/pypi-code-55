# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydbfill']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.1.0,<5.0.0', 'pymysql>=0.9.3,<0.10.0', 'pytest>=5.4.2,<6.0.0']

setup_kwargs = {
    'name': 'pydbfill',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Oren Mazor',
    'author_email': 'oren.mazor@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
