# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotcp']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.4,<2.0.0']

setup_kwargs = {
    'name': 'plotcp',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Winkel',
    'author_email': 'dmesser@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
