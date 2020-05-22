# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aicloud']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aicloud',
    'version': '0.0.2',
    'description': '',
    'long_description': '# aicloud',
    'author': 'AI Sbercloud team',
    'author_email': 'support@sbercloud.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aicloud.sbercloud.ru/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
