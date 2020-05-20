# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openevsewifi']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.10,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'openevsewifi',
    'version': '1.0.0',
    'description': 'A python library for communicating with the ESP8266-based wifi module from OpenEVSE',
    'long_description': '# python-openevse-wifi\nA python library for communicating with the ESP8266-based wifi module from OpenEVSE\n',
    'author': 'Michelle Avery',
    'author_email': 'dev@miniconfig.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miniconfig/python-openevse-wifi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
