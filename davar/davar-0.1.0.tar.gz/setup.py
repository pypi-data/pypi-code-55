# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['davar']

package_data = \
{'': ['*']}

install_requires = \
['arpeggio>=1.9.2,<2.0.0', 'wikidata>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'davar',
    'version': '0.1.0',
    'description': 'An experimental interpreted international auxiliary language.',
    'long_description': None,
    'author': 'Impossibly New',
    'author_email': 'newlyimpossible@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
