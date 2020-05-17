# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mason', 'mason.nodes', 'mason.proto']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'protobuf>=3.11.3,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'mason-framework',
    'version': '0.0.3',
    'description': 'Node based building blocks.',
    'long_description': None,
    'author': 'Eric Hulser',
    'author_email': 'eric.hulser@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
