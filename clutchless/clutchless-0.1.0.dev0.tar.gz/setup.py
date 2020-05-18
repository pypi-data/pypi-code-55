# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutchless',
 'clutchless.message',
 'clutchless.parse',
 'clutchless.subcommand']

package_data = \
{'': ['*']}

install_requires = \
['bencode.py>=2.1.0,<3.0.0',
 'colorama>=0.4.3,<0.5.0',
 'docopt>=0.6.2,<0.7.0',
 'texttable>=1.6.2,<2.0.0',
 'torrentool>=1.0.2,<2.0.0',
 'transmission-clutch>=3.1.1,<4.0.0']

entry_points = \
{'console_scripts': ['clutchless = clutchless.console:main']}

setup_kwargs = {
    'name': 'clutchless',
    'version': '0.1.0.dev0',
    'description': 'A CLI tool for importing data into the Transmission BitTorrent client',
    'long_description': None,
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
