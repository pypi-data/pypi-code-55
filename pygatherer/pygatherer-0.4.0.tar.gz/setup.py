# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygatherer', 'pygatherer.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.0.0,<5.0.0', 'lxml>=4.0.0,<5.0.0', 'requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pygatherer',
    'version': '0.4.0',
    'description': 'An API for the gatherer',
    'long_description': '<p align="center">\n<a href="https://travis-ci.org/spapanik/pygatherer"><img alt="Build" src="https://travis-ci.org/spapanik/pygatherer.svg?branch=master"></a>\n<a href="https://coveralls.io/github/spapanik/pygatherer"><img alt="Coverage" src="https://coveralls.io/repos/github/spapanik/pygatherer/badge.svg?branch=master"></a>\n<a href="https://github.com/spapanik/pygatherer/blob/master/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/pygatherer"></a>\n<a href="https://pypi.org/project/pygatherer"><img alt="PyPI" src="https://img.shields.io/pypi/v/pygatherer"></a>\n<a href="https://pepy.tech/project/pygatherer"><img alt="Downloads" src="https://pepy.tech/badge/pygatherer"></a>\n<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nInstallation\n------------\n\nYou can install pygatherer directly with pip:\n\n    $ pip install pygatherer\n',
    'author': 'Stephanos Kuma',
    'author_email': 'spapanik21@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/pygatherer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
