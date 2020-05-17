# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pingtest']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'command>=0.1.0,<0.2.0',
 'matplotlib>=3.1.3,<4.0.0',
 'mysql.connector>=2.2.9,<3.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'pingtest',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Colin Boyd',
    'author_email': 'csboyd@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
