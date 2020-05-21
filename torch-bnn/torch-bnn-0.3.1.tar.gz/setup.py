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
    'version': '0.3.1',
    'description': 'Library implementing Bayesian Neural Networks in pytorch',
    'long_description': None,
    'author': 'Antoine Lefebvre-Brossard',
    'author_email': 'antoinelb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
