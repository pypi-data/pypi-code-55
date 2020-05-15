# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_cache']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.10.0,<3.0.0', 'numpy', 'pandas>=1.0.0,<2.0.0', 'tables']

setup_kwargs = {
    'name': 'data-cache',
    'version': '0.1.4',
    'description': 'Data Cache',
    'long_description': None,
    'author': 'Statnett Datascience',
    'author_email': 'Datascience.Drift@statnett.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
