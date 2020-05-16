# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpattern']

package_data = \
{'': ['*']}

install_requires = \
['pipetools>=0.3.5,<0.4.0']

setup_kwargs = {
    'name': 'xpattern',
    'version': '0.1.0',
    'description': 'The Pattern Matching for Python',
    'long_description': None,
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
