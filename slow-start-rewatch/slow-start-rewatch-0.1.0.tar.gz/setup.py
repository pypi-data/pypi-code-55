# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slow_start_rewatch']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'importlib_metadata>=1.6.0,<2.0.0']

entry_points = \
{'console_scripts': ['slow-start-rewatch = slow_start_rewatch.__main__:main']}

setup_kwargs = {
    'name': 'slow-start-rewatch',
    'version': '0.1.0',
    'description': 'Make cute things happen!',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/slow-start-fans/slow-start-rewatch/master/assets/happy_shion.gif" width="384" height="360" />\n</p>\n\n\n# Slow Start Rewatch\n\n[![Build Status](https://travis-ci.org/slow-start-fans/slow-start-rewatch.svg?branch=master)](https://travis-ci.org/slow-start-fans/slow-start-rewatch)\n[![Coverage](https://coveralls.io/repos/github/slow-start-fans/slow-start-rewatch/badge.svg?branch=master)](https://coveralls.io/github/slow-start-fans/slow-start-rewatch?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/slow-start-rewatch.svg)](https://pypi.org/project/slow-start-rewatch/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n## Missions\n\nMake cute things happen!\n\nProvide a command-line utility for hosting an awesome Slow Start Rewatch.\n\n\n## Features\n\n- Schedule a submission of Reddit posts (TBD)\n- Templates-based posts (TBD)\n- Reddit authorization via OAuth2 using a local HTTP server with cute GIFs (TBD)\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n\n\n## Installation\n\n```bash\npip install slow-start-rewatch\n```\n\n\n## Usage\n\nLaunch the program from the command line:\n\n```bash\nslow-start-rewatch\n```\n\n## License\n\n[MIT](https://github.com/slow-start-fans/slow-start-rewatch/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package).\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slow-start-fans/slow-start-rewatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
