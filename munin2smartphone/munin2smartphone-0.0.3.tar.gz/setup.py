# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['munin2smartphone']

package_data = \
{'': ['*'], 'munin2smartphone': ['templates/*']}

install_requires = \
['PyYAML==5.3.1',
 'aiohttp==3.6.2',
 'coloredlogs>=14.0,<15.0',
 'jinja2>=2.11.2,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'pyxdg>=0.26,<0.27',
 'quicklogging>=0.3,<0.4',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['munin2smartphone = '
                     'munin2smartphone.entrypoints:run_from_cli']}

setup_kwargs = {
    'name': 'munin2smartphone',
    'version': '0.0.3',
    'description': 'HTTP API producing static pages from your munin data',
    'long_description': '================\nmunin2smartphone\n================\n\nDemilitarized HTTP server producing static pages that can be displayed securely (ie. without javascript).\n\n.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/\n\n.. |license-GPL-2| image::  https://img.shields.io/badge/license-GPL%202-informational\n   :target: https://framagit.org/feth/munin2smartphone/-/blob/master/LICENSE_GPL_2.txt\n\n.. |license-CeCILL-2.1| image::  https://img.shields.io/badge/license-CeCILL--2.1-informational\n   :target: https://framagit.org/feth/munin2smartphone/-/blob/LICENSE_CeCILL_2.1.txt\n\n.. |project-url| image:: https://img.shields.io/badge/homepage-framagit-blue\n   :target: https://framagit.org/feth/munin2smartphone\n\n.. |repository-url| image:: https://img.shields.io/badge/repository-git%2Bhttps-blue\n   :target: https://framagit.org/feth/munin2smartphone.git\n\n.. |documentation| image:: https://readthedocs.org/projects/munin2smartphone/badge/?version=latest   :alt: Read the Docs\n\n|made-with-python| |license-GPL-2| |license-CeCILL-2.1| |project-url| |repository-url|\n\n.. figure:: docs/images/screenshot_android.png\n\n   Screen capture of *munin2smartphone* on an android phone.\n\nInstallation, usage and development documentation: |documentation|\n\ndocumentation = "https://munin2smartphone.readthedocs.io/"\n\n',
    'author': 'Feth AREZKI',
    'author_email': 'feth@majerti.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/feth/munin2smartphone',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
