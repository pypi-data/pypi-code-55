# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdistributionpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pdistributionpy',
    'version': '0.1',
    'description': 'A python package for Gaussian and binomial distribution',
    'long_description': '## Gausian Distribution and Binomial distribution\n\n- A python package for binomial and gaussian distribution\n\n',
    'author': 'Bhagawan Subedi',
    'author_email': 'bhag1subedi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
