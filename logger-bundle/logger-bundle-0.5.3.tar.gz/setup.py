# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['loggerbundle']

package_data = \
{'': ['*'], 'loggerbundle': ['_config/*', 'extra/*', 'handler/*', 'stdout/*']}

install_requires = \
['colorlog>=4.0.0,<4.1.0', 'pyfony-bundles>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'logger-bundle',
    'version': '0.5.3',
    'description': 'Logger bundle for the Pyfony framework',
    'long_description': 'Logger bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/logger-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
