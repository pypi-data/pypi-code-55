# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whale_back_bone', 'whale_back_bone.mysql_connection']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=0.9.3,<0.10.0', 'pandas>=1.0.3,<2.0.0', 'sqlalchemy>=1.3.17,<2.0.0']

setup_kwargs = {
    'name': 'whale-back-bone',
    'version': '0.1.0',
    'description': ' This library is aimed to create a MySQL connector that could be used by the 4th Whale Marketing data team.',
    'long_description': None,
    'author': 'Arnaud Pourchez',
    'author_email': 'arnaud.pourchez@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
