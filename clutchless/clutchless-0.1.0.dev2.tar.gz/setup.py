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
    'version': '0.1.0.dev2',
    'description': 'A CLI tool to manage torrents and their data in Transmission',
    'long_description': "**This is still under active development - use at your own risk!**\n\nClutchless\n----------\n\n.. image:: https://readthedocs.org/projects/clutch/badge/?version=latest\n    :target: https://clutch.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation badge\n\n.. image:: https://img.shields.io/pypi/v/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI badge\n\n.. image:: https://img.shields.io/pypi/pyversions/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI versions badge\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Black formatter badge\n\n.. image:: https://img.shields.io/pypi/l/clutchless.svg\n    :target: https://en.wikipedia.org/wiki/MIT_License\n    :alt: License badge\n\n.. image:: https://img.shields.io/pypi/dm/clutchless.svg\n    :target: https://pypistats.org/packages/clutchless\n    :alt: PyPI downloads badge\n\nQuick start\n===========\n\nInstall the package:\n\n.. code-block:: console\n\n    $ pip install clutchless\n\nThe ``-h`` flag can be used to bring up documentation, e.g. ``clutchless -h``::\n\n    A tool for working with torrents and their data in the Transmission BitTorrent client.\n\n    Usage:\n        clutchless [options] <command> [<args> ...]\n\n    Options:\n        -h, --help  Show this screen.\n        --version   Show version.\n\n    The available clutchless commands are:\n        add         Add torrents to Transmission (with or without data).\n        find        Locate data that belongs to torrent files.\n        link        For torrents with missing data in Transmission, find the data and fix the location.\n        archive     Copy .torrent files from Transmission for backup.\n        organize    Migrate torrents to a new location, sorting them into separate folders for each tracker.\n\n    See 'clutchless help <command>' for more information on a specific command.\n",
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mhadam/clutchless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
