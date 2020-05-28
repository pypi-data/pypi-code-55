# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pma']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['pma = pma.cli:cli']}

setup_kwargs = {
    'name': 'pma',
    'version': '2.0.1',
    'description': 'Farm points on PiXL Maths App',
    'long_description': "# PiXL Maths App Farm\n[![Tests](https://github.com/nihaals/pixl-maths-app-farm/workflows/Tests/badge.svg)](https://github.com/nihaals/pixl-maths-app-farm/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/nihaals/pixl-maths-app-farm/branch/master/graph/badge.svg)](https://codecov.io/gh/nihaals/pixl-maths-app-farm)\n[![PyPI](https://img.shields.io/pypi/v/PMA)](https://pypi.org/project/PMA/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PMA)](https://pypi.org/project/PMA/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/PMA)](https://pypi.org/project/PMA/)\n\nThis project requires at least Python 3.8.\nThe tool is designed to work with [PiXL's Maths App](https://mathsapp.pixl.org.uk/PMA2.html).\nIt was created by reverse engineering the flash file and took a huge amount of time so any\nsupport is appreciated.\n\n## Setup\n1. Install [Python](https://www.python.org/downloads/)\n2. Run `pip install -U pma` in your terminal/command prompt. This is the same command to update\n\nThere are also docker images on [GitHub](https://github.com/nihaals/pixl-maths-app-farm/packages) and [Docker Hub](https://hub.docker.com/r/orangutan/pma).\n\n## CLI Usage\n* `pma farm --help`\n* `python -m pma farm --help`\n* `python -m pma farm --goal 100 SCHOOL_ID USERNAME PASSWORD`\n* `python -m pma farm --yes SCHOOL_ID USERNAME PASSWORD`\n* `python -m pma farm --goal 100 --yes SCHOOL_ID USERNAME PASSWORD`\n* `python -m pma farm SCHOOL_ID USERNAME PASSWORD`\n\nNote: You can use either `pma` or `python -m pma`\n",
    'author': 'Nihaal Sangha',
    'author_email': 'me@niha.al',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nihaals/pixl-maths-app-farm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
