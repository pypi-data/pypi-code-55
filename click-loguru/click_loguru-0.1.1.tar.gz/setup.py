# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_loguru']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'flynt>=0.46.1,<0.47.0', 'loguru>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'click-loguru',
    'version': '0.1.1',
    'description': 'Configure loguru logging for use with click.',
    'long_description': '',
    'author': 'Joel Berendzen',
    'author_email': 'joel@generisbio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/legumeinfo/bionorm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
