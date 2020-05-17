# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sardine',
 'sardine.actions',
 'sardine.exceptions',
 'sardine.exceptions.lang',
 'sardine.exceptions.lang.manifest',
 'sardine.exceptions.lang.parser',
 'sardine.exceptions.lang.tokenizer',
 'sardine.lang',
 'sardine.lang.manifest',
 'sardine.lang.parser',
 'sardine.lang.tokenizer',
 'sardine.resolvers',
 'sardine.resolvers.manifest',
 'sardine.resolvers.repository']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'sardine',
    'version': '0.0.0a0',
    'description': 'Manage your docker-composes as if they were snipets',
    'long_description': None,
    'author': 'Javier Luna molina',
    'author_email': 'javierlunamolina@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
