# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kharser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kharser',
    'version': '0.1.1',
    'description': 'parse stuff',
    'long_description': '# Kharser\n\n',
    'author': 'KhalidCK',
    'author_email': 'fr.ckhalid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
