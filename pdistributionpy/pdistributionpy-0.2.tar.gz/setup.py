# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdistributionpy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==1.3.1']

setup_kwargs = {
    'name': 'pdistributionpy',
    'version': '0.2',
    'description': 'A python package for Gaussian and binomial distribution',
    'long_description': '## Gausian Distribution and Binomial distribution\n\n- A python package for binomial and gaussian distribution\n\n',
    'author': 'Bhagawan Subedi',
    'author_email': 'bhag1subedi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
