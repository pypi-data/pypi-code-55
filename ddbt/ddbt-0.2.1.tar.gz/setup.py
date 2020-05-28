# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ddbt', 'ddbt.extra', 'ddbt.task']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'dbt>=0.16.0,<0.17.0',
 'hvac[parser]>=0.10.2,<0.11.0',
 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['ddbt = ddbt.cli:main']}

setup_kwargs = {
    'name': 'ddbt',
    'version': '0.2.1',
    'description': 'Command line tool that adds E (extract), L (load) and some other extra dev features to dbt (https://www.getdbt.com).',
    'long_description': '# TODO\n',
    'author': 'Radek Tomsej',
    'author_email': 'radek@tomsej.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomsej/ddbt/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
