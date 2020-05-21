# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discordrp_pcsx2n']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'pypresence>=3.3,<4.0']

entry_points = \
{'console_scripts': ['discordrp-pcsx2n = discordrp_pcsx2n:main']}

setup_kwargs = {
    'name': 'discordrp-pcsx2n',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Discord Rich Presence for PCSX2\n[![Downloads](https://pepy.tech/badge/discordrp-pcsx2)](https://pepy.tech/project/discordrp-pcsx2)\n## Installation: \n```bash\npip install discordrp-pcsx2\n```\n\n## Usage\n```\n$ discordrp-pcsx2 --help\nDiscord Rich Presence support for PCSX2.\n\nUsage:\n    discordrp-pcsx2 [--path=<path>]\n\nOptions:\n    --path=<path> Path to your PCSX2 directory, optional.\n```\n\n**discordrp-pcsx2** is still very early in development, so feel free to report any issues [here!](https://github.com/AnonGuy/discordrp-pcsx2/issues/new)\n\n## Examples\n![image](https://i.imgur.com/clvQA9q.png)\n![image](https://i.imgur.com/56GT4VC.png)\n![image](https://i.imgur.com/NP10O3o.png)\n\n## Cover Art\nDue to the nature of Rich Presence assets, Images that are used for cover art must be added by me manually. [Create an issue](https://github.com/AnonGuy/discordrp-pcsx2/issues/new) if you would like to suggest cover art for a specific game.\n',
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
