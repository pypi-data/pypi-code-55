# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monetdb_pystethoscope', 'monetdb_pystethoscope.connection']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pymonetdb>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['pystethoscope = '
                     'monetdb_pystethoscope.stethoscope:stethoscope']}

setup_kwargs = {
    'name': 'monetdb-pystethoscope',
    'version': '0.1.3',
    'description': 'MonetDB profiler connection tool',
    'long_description': '|PyPIBadge|_ |ActionsBadge|_ |DocsBadge|_ |CoverageBadge|_\n\nIntroduction\n============\n\n``pystethoscope`` is a command line tool to filter and format the events coming\nfrom the MonetDB profiler. The profiler is part of the MonetDB server and works\nby emitting two JSON objects: one at the start and one at the end of every MAL\ninstruction executed. ``pystethoscope`` connects to a MonetDB server process,\nreads the objects emitted by the profiler and performs various transformations\nspecified by the user.\n\nInstallation\n============\n\nInstallation is done via pip:\n\n.. code:: shell\n\n   pip install monetdb-pystethoscope\n\nThis project is compatible with Python 3.5 or later and with MonetDB server\nversion Jun2020 or later.\n\nWe recommend the use of virtual environments (see `this\nprimer <https://realpython.com/python-virtual-environments-a-primer/>`__\nif you are unfamiliar) for installing and using\n``monetdb-pystethoscope``.\n\nDeveloper notes\n===============\n\n``pystethoscope`` is developed using\n`Poetry <https://python-poetry.org/>`__, for dependency management and\npackaging.\n\nInstallation for development\n----------------------------\n\nIn order to install ``pystethoscope`` do the following:\n\n.. code:: shell\n\n   pip3 install --user poetry\n   PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"\n   export PATH="$PATH:$PYTHON_BIN_PATH"\n\n   git clone git@github.com:MonetDBSolutions/monetdb-pystethoscope.git\n   cd monetdb-pystethoscope\n   poetry install\n   poetry run pystethoscope --help\n\nDocumentation\n=============\n\nFor more detailed documentation please see the documentation on `readthedocs\n<https://monetdb-pystethoscope.readthedocs.io/en/latest/>`__.\n\n.. |ActionsBadge| image:: https://github.com/MonetDBSolutions/monetdb-pystethoscope/workflows/Test%20pystethoscope/badge.svg?branch=master\n.. _ActionsBadge: https://github.com/MonetDBSolutions/monetdb-pystethoscope/actions\n.. |DocsBadge| image:: https://readthedocs.org/projects/monetdb-pystethoscope/badge/?version=latest\n.. _DocsBadge: https://monetdb-pystethoscope.readthedocs.io/en/latest/?badge=latest\n.. |CoverageBadge| image:: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope/branch/master/graph/badge.svg\n.. _CoverageBadge: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope\n.. |PyPIBadge| image:: https://img.shields.io/pypi/v/monetdb-pystethoscope.svg\n.. _PyPIBadge: https://pypi.org/project/monetdb-pystethoscope/\n',
    'author': 'Panagiotis Koutsourakis',
    'author_email': 'kutsurak@monetdbsolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MonetDBSolutions/monetdb-pystethoscope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
