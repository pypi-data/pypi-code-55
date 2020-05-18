# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytbot']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pyppeteer_stealth>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['ytbot = ytbot:main']}

setup_kwargs = {
    'name': 'ytbot',
    'version': '0.2.3',
    'description': 'A simple yet amazing bot for increasing youtube views and it works!!',
    'long_description': '',
    'author': 'Muhammad Fahim',
    'author_email': 'muhammadfahim010@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adnangif/ytbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
