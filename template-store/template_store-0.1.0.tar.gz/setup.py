# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['template_store']

package_data = \
{'': ['*']}

install_requires = \
['grpcio', 'grpcio-tools']

setup_kwargs = {
    'name': 'template-store',
    'version': '0.1.0',
    'description': 'lumoz.ai brick templates store',
    'long_description': None,
    'author': 'Attinad Software',
    'author_email': 'attinad@attinadsoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
