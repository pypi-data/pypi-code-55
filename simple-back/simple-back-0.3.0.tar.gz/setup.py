# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_back']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pandas_market_calendars>=1.3.5,<2.0.0',
 'requests_html>=0.10.0,<0.11.0',
 'yahoo_fin>=0.8.5,<0.9.0']

setup_kwargs = {
    'name': 'simple-back',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Christoph Minixhofer',
    'author_email': 'christoph.minixhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
