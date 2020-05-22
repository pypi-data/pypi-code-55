# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbplugins_watch']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'nonebot>=1.6.0,<2.0.0', 'watchgod>=0.6,<0.7']

setup_kwargs = {
    'name': 'nbplugins-watch',
    'version': '0.0.1',
    'description': 'watch and (re)load plugins from a directory',
    'long_description': None,
    'author': 'ffreemt',
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
