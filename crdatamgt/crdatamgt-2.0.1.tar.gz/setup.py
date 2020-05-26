# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crdatamgt']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'simplelogging>=0.10.0,<0.11.0',
 'toolz>=0.10.0,<0.11.0',
 'xlsxwriter>=1.2.8,<2.0.0']

setup_kwargs = {
    'name': 'crdatamgt',
    'version': '2.0.1',
    'description': 'Chemistry research data management application',
    'long_description': None,
    'author': 'Michael Jaquier',
    'author_email': 'michael.jaquier@contracted.pmi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
