# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['SandsPythonFunctions']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'black>=19.10b0,<20.0',
 'bs4>=0.0.1,<0.0.2',
 'flake8>=3.8.1,<4.0.0',
 'nltk>=3.5,<4.0',
 'notebook>=6.0.3,<7.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.0,<5.0.0',
 'zstandard>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'sandspythonfunctions',
    'version': '0.0.1a3',
    'description': 'Functions I use regularly with my python projects',
    'long_description': '# Sands Python Functions\n\nSome functions I find useful regularly and I put them all into one package for easy access\n\nI created this using [Poetry](https://python-poetry.org/).\n',
    'author': 'ldsands',
    'author_email': 'ldsands@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ldsands/SandsPythonFunctions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
