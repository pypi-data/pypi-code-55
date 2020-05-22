# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml2instance']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'flake8>=3.8.1,<4.0.0',
 'mypy>=0.770,<0.771',
 'pytest>=5.4.2,<6.0.0',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'yaml2instance',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'shuns0314',
    'author_email': 'shunsuke.naka0314@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
