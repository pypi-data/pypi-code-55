# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okerr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'okerr',
    'version': '0.1.3',
    'description': 'A simple Result with match functionality for Python',
    'long_description': "okerr\n=====\n\n.. image:: https://img.shields.io/github/license/ceb10n/okerr\n    :target: https://img.shields.io/github/license/ceb10n/okerr\n\n.. image:: https://circleci.com/gh/ceb10n/okerr.svg?style=shield\n    :target: https://circleci.com/gh/ceb10n/okerr\n\n.. image:: https://codecov.io/gh/ceb10n/okerr/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/ceb10n/okerr\n\nA simple Result with match functionality for Python 3 inspired by `Rust's Result Enum\n<https://doc.rust-lang.org/std/result/>`__.\n\n\nLicense\n-------\n\nMIT License\n",
    'author': 'Rafael Marques',
    'author_email': 'rafaelomarques@gmail.com',
    'maintainer': 'Rafael Marques',
    'maintainer_email': 'rafaelomarques@gmail.com',
    'url': 'https://github.com/ceb10n/okerr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
