# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['SandsPythonFunctions']

package_data = \
{'': ['*']}

install_requires = \
['notebook>=6.0.3,<7.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'zstandard>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'sandspythonfunctions',
    'version': '0.0.1a5',
    'description': 'Functions I use regularly with my python projects',
    'long_description': "# Sands Python Functions\n\nSome functions I find useful regularly and I put them all into one package for easy access\n\nI created this using [Poetry](https://python-poetry.org/).\n\n## Instructions\n\n- To build this you must first install poetry see instructions [here](https://python-poetry.org/docs/#installation)\n- However to make it easy to access this is all of the code you'll need on linux to make this run (note that I use zsh not bash for my shell)\n\n```zsh\nTODO:\n```\n\n## Basic Usage Example\n\nTODO:\n\n## Testing\n\nPytest runs in whatever directory you're located in at the time you run pytest so if you're not in the directory of the test scripts pytest will not see the files it needs to and will then fail.\n",
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
