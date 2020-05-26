# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpenv',
 'cpenv.repos',
 'cpenv.vendor',
 'cpenv.vendor.cachetools',
 'cpenv.vendor.yaml',
 'cpenv.vendor.yaml.yaml2',
 'cpenv.vendor.yaml.yaml3']

package_data = \
{'': ['*'], 'cpenv': ['bin/*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'psutil>=5.7.0,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['cpenv = cpenv.__main__:main']}

setup_kwargs = {
    'name': 'cpenv',
    'version': '0.5.4',
    'description': 'Cross-platform module and environment management.',
    'long_description': None,
    'author': 'Dan Bradham',
    'author_email': 'danielbradham@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
