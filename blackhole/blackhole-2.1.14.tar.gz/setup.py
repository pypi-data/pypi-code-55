# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackhole']

package_data = \
{'': ['*']}

install_requires = \
['coverage[dev,tests]>=5.1,<6.0',
 'guzzle_sphinx_theme[dev,docs]>=0.7.11,<0.8.0',
 'pre-commit[dev]>=2.4.0,<3.0.0',
 'pytest-asyncio[dev,tests]>=0.12.0,<0.13.0',
 'pytest-clarity[dev,tests]>=0.3.0-alpha.0,<0.4.0',
 'pytest-cov[dev,tests]>=2.8.1,<3.0.0',
 'pytest[dev,tests]>=5.4.2,<6.0.0',
 'setproctitle[setproctitle]>=1.1.10,<2.0.0',
 'sphinx[dev,docs]>=3.0.3,<4.0.0',
 'tox[dev]>=3.15.0,<4.0.0',
 'uvloop[uvloop]>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'blackhole',
    'version': '2.1.14',
    'description': 'Blackhole is an MTA (message transfer agent) that (figuratively) pipes all mail to /dev/null.',
    'long_description': None,
    'author': 'Kura',
    'author_email': 'kura@kura.gg',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6.1,<4',
}


setup(**setup_kwargs)
