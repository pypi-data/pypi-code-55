# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocrontab']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=0.3.31,<0.4.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing_extensions']}

setup_kwargs = {
    'name': 'aiocrontab',
    'version': '0.1.0',
    'description': 'Crontab implementation in asyncio ',
    'long_description': None,
    'author': 'Bhavesh Praveen',
    'author_email': 'bhavespraveen.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
