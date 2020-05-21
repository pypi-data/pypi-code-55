# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schemahq']

package_data = \
{'': ['*']}

install_requires = \
['colorful>=0.5.4,<0.6.0',
 'fire>=0.3.0,<0.4.0',
 'pgformatter>=0.1.5,<0.2.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'schemahq-migra>=1.0.10,<2.0.0',
 'sqlbag>=0.1.1579049654,<0.2.0',
 'sqlparse>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['schemahq = schemahq.cli:main']}

setup_kwargs = {
    'name': 'schemahq',
    'version': '0.1.13',
    'description': '',
    'long_description': None,
    'author': 'Nathan Cahill',
    'author_email': 'nathan@nathancahill.com',
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
