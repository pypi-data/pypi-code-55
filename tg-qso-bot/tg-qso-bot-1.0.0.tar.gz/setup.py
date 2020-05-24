# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_qso_bot', 'tg_qso_bot.bot', 'tg_qso_bot.models', 'tg_qso_bot.qso_sources']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'pyrogram>=0.17.1,<0.18.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tg-qso-bot',
    'version': '1.0.0',
    'description': 'Simple HAM helper bot written on Python',
    'long_description': None,
    'author': 'exepirit',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
