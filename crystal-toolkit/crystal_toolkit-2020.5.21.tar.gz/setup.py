# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal_toolkit',
 'crystal_toolkit.apps',
 'crystal_toolkit.apps.examples',
 'crystal_toolkit.apps.examples.tests',
 'crystal_toolkit.apps.tests',
 'crystal_toolkit.components',
 'crystal_toolkit.components.transformations',
 'crystal_toolkit.core',
 'crystal_toolkit.core.tests',
 'crystal_toolkit.helpers',
 'crystal_toolkit.renderables']

package_data = \
{'': ['*'], 'crystal_toolkit.apps': ['assets/*']}

install_requires = \
['Flask-Caching>=1.8.0,<2.0.0',
 'dash-daq>=0.4.0,<0.5.0',
 'dash>=1.12.0,<2.0.0',
 'dash_mp_components>=0.0.21,<0.0.22',
 'gevent>=1.4.0,<2.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'habanero>=0.7.2,<0.8.0',
 'hiphive>=0.7,<0.8',
 'plotly>=4.5.4,<5.0.0',
 'pydantic>=1.4,<2.0',
 'pymatgen>=2020.4.29,<2021.0.0',
 'redis>=3.4.1,<4.0.0',
 'robocrys>=0.2.1,<0.3.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'webcolors>=1.11.1,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=3.7,<4.0']}

setup_kwargs = {
    'name': 'crystal-toolkit',
    'version': '2020.5.21',
    'description': '',
    'long_description': None,
    'author': 'Matthew Horton',
    'author_email': 'mkhorton@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
