# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betterls']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['bls = betterls.ls:bls']}

setup_kwargs = {
    'name': 'betterls',
    'version': '1.3.1',
    'description': 'Better ls command.',
    'long_description': "# BetterLS [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FRealCyGuy%2Fbetterls)](https://twitter.com/intent/tweet?text=This%20is%20hands%20down%20the%20BEST%20GitHub%20repo%20in%20the%20entirety%20of%20GitHub.%20Just%20very%2C%20very%2C%20very%2C%20very%2C%20very%2C%20very%20amazing.%20You%20should%20definitely%20check%20them%20out:&url=https%3A%2F%2Fgithub.com%2FRealCyGuy%2Fbetterls)\n\n*A better ls command than windows `dir`. Not sure about linux though. :|*\n\n[![PyPI](https://img.shields.io/pypi/v/betterls?label=latest%20version&style=for-the-badge)](https://pypi.org/project/betterls/#history)\n[![PyPI - Downloads](https://img.shields.io/pypi/dd/betterls?style=for-the-badge)](https://pypi.org/project/betterls)\n[![GitHub license](https://img.shields.io/github/license/realcyguy/betterls?style=for-the-badge)](https://github.com/RealCyGuy/betterls/blob/master/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/realcyguy/betterls?style=for-the-badge)](https://github.com/realcyguy/betterls/issues)\n\nLook how cool:\n![bls](https://i.imgur.com/5EzMyjX.png)\n\n## Installation\n\nUse [PIP](https://pypi.org/project/betterls/):\n\n```bash\n$ pip install --upgrade betterls\n```\n\n## Usage\n\nIf you're on Windows, use a ANSI escape code compatible terminal (like Windows Terminal) or use `--no-ansi`/`-na`.\n\n```\nUsage: bls [OPTIONS]\n\nOptions:\n  -nc, --no-colour  Disable colours.\n  -hm, --heat-map   Heat map based on file size.\n  -na, --no-ansi    Make colours work on non-ansi supported terminals, but not\n                    underlines.\n\n  -h, --help        Show this message and exit.\n```\n\n## Features\n\n- Auto-columns.\n- Highlight for different file types.\n- List out files.\n- Heat map.\n- A help command.\n- Support for non-ansi terminals.\n\n## License\n\n[MIT](https://github.com/RealCyGuy/betterls/blob/master/LICENSE) license.\n",
    'author': 'Cyrus Yip',
    'author_email': 'cyruscmyip1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RealCyGuy/betterls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
