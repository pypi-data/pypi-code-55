# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_gridworld']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.13,<2.0', 'py-aiger-bv>=4.0.0,<5.0.0', 'py-aiger>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'py-aiger-gridworld',
    'version': '0.3.0',
    'description': 'Library for modeling gridworlds as AIGER circuits.',
    'long_description': '# py-aiger-gridworld\n\nLibrary for modeling gridworlds as AIGER circuits.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-gridworld/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-gridworld)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-gridworld/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-gridworld)\n[![PyPI version](https://badge.fury.io/py/py-aiger-gridworld.svg)](https://badge.fury.io/py/py-aiger-gridworld)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<object data="assets/visualization_example.svg" type="image/svg+xml">\n  <img src="assets/visualization_example.svg" />\n</object>\n\n# Installation\n\nIf you just need to use `aiger_gridworld`, you can just run:\n\n`$ pip install py-aiger-gridwolrd`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
