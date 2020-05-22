# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_squeeze']

package_data = \
{'': ['*']}

install_requires = \
['brotli>=1.0.7,<2.0.0',
 'flask>=1.1.2,<2.0.0',
 'rcssmin>=1.0.6,<2.0.0',
 'rjsmin>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'flask-squeeze',
    'version': '1.8',
    'description': 'Compress and minify Flask responses!',
    'long_description': None,
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
