# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchdataset']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0', 'sox>=1.3.7,<2.0.0', 'torch>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'torchdataset',
    'version': '0.1.0',
    'description': 'This is a package to handle various kinds of data in a unified way with Pytorch.',
    'long_description': None,
    'author': 'popura',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
