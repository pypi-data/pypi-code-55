# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ujimaru_text_generate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ujimaru-text-generate',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hppRC/ujimaru',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
