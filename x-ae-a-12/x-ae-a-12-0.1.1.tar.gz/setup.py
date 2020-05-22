# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['x_ae_a_12']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.0,<4.0.0',
 'pytest-mock>=3.1.0,<4.0.0',
 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['x-ae-a-12 = x_ae_a_12.console:main']}

setup_kwargs = {
    'name': 'x-ae-a-12',
    'version': '0.1.1',
    'description': 'The X-AE-A-12 Python project',
    'long_description': '# X-AE-A-12\n\n[![Tests](https://github.com/SpencerOfwiti/X-AE-A-12/workflows/Tests/badge.svg)](https://github.com/SpencerOfwiti/X-AE-A-12/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/SpencerOfwiti/X-AE-A-12/branch/master/graph/badge.svg)](https://codecov.io/gh/SpencerOfwiti/X-AE-A-12)\n[![PyPI](https://img.shields.io/pypi/v/x-ae-a-12.svg)](https://pypi.org/project/x-ae-a-12/)\n[![Read the Docs](https://readthedocs.org/projects/x-ae-a-12/badge/)](https://x-ae-a-12.readthedocs.io/)\n\nCommand line application for displaying random facts from wikipedia on the console.\n',
    'author': 'Spencer Ofwiti',
    'author_email': 'maxspencer56@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SpencerOfwiti/X-AE-A-12',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
