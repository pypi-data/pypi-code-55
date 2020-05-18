# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nujo',
 'nujo.autodiff',
 'nujo.autodiff._functions',
 'nujo.init',
 'nujo.math',
 'nujo.nn',
 'nujo.objective',
 'nujo.optim',
 'nujo.utils',
 'nujo.utils.data',
 'nujo.utils.viz']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.13.2,<0.14.0',
 'numpy>=1.18.1,<2.0.0',
 'pillow>=7.1.2,<8.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'nujo',
    'version': '0.2.0',
    'description': 'A Reverse-mode Automatic Differentiation library for Neural Networks',
    'long_description': None,
    'author': 'Victor Velev',
    'author_email': 'victorivelev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
