# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_bnn', 'torch_bnn.bnn', 'torch_bnn.bnn.rnn']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'torch']

setup_kwargs = {
    'name': 'torch-bnn',
    'version': '0.3.8',
    'description': 'Library implementing Bayesian Neural Networks in pytorch',
    'long_description': '[![pipeline status](https://gitlab.com/antoinelb/torch-bnn/badges/master/pipeline.svg)](https://gitlab.com/antoinelb/torch-bnn/-/commits/master)\n[![coverage report](https://gitlab.com/antoinelb/torch-bnn/badges/master/coverage.svg)](https://gitlab.com/antoinelb/torch-bnn/-/commits/master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n\n# Pytorch Bayesian Neural Networks\n\nImplements a series of bayesian layers for use in bayesian neural networks.\n',
    'author': 'Antoine Lefebvre-Brossard',
    'author_email': 'antoinelb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/antoinelb/torch-bnn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
