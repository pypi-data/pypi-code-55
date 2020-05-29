# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirai_translate']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'httpx>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'mirai-translate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'reiyw',
    'author_email': 'reiyw.setuve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
