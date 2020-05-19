# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['movie_colorbar']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0', 'loguru>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'movie-colorbar',
    'version': '0.1.0',
    'description': 'Turn a video into a colorbar',
    'long_description': None,
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
