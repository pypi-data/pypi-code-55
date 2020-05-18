# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_data_transfer']

package_data = \
{'': ['*']}

install_requires = \
['redis-py-cluster>=2.0.0,<2.1.0', 'setproctitle>=1.1.10,<1.2.0']

entry_points = \
{'console_scripts': ['redis-data-transfer = redis_data_transfer:main']}

setup_kwargs = {
    'name': 'redis-data-transfer',
    'version': '0.2.0',
    'description': 'Transfer data between a redis instances or clusters',
    'long_description': None,
    'author': 'EDITED Devs',
    'author_email': 'dev@edited.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
