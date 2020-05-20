# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_js']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'funcy>=1.14,<2.0',
 'py-aiger-ptltl>=3.0.0,<4.0.0',
 'py-aiger>=6.0.0,<7.0.0',
 'pytest-flake8>=1.0.6,<2.0.0',
 'pytest-xdist>=1.32.0,<2.0.0']

setup_kwargs = {
    'name': 'py-aiger-js',
    'version': '0.1.1',
    'description': 'A Python library for compiling AIGs to Javascript.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
