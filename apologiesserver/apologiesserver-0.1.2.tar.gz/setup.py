# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apologiesserver']

package_data = \
{'': ['*']}

install_requires = \
['apologies>=0.1.16,<0.2.0',
 'asyncio-periodic>=2019.2,<2020.0',
 'ordered-set>=4.0.1,<5.0.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'apologiesserver',
    'version': '0.1.2',
    'description': 'Websocket server to interactively play the Apologies game',
    'long_description': '# Apologies Server\n\n![](https://img.shields.io/pypi/l/apologiesserver.svg)\n![](https://img.shields.io/pypi/wheel/apologiesserver.svg)\n![](https://img.shields.io/pypi/pyversions/apologiesserver.svg)\n![](https://github.com/pronovic/apologies-server/workflows/Test%20Suite/badge.svg)\n![](https://readthedocs.org/projects/apologies-server/badge/?version=latest&style=flat)\n\n[Apologies Server](https://github.com/pronovic/apologies-server) is a [Websocket](https://en.wikipedia.org/wiki/WebSocket) server interface used to interactively play a multi-player game using the [Apologies](https://github.com/pronovic/apologies) library.  The Apologies library implements a game similar to the [Sorry](https://en.wikipedia.org/wiki/Sorry!_(game)) board game.  See the [documentation](https://apologies-server.readthedocs.io/en/latest) for notes about the public interface and the event model.\n\n_Note:_ At present, the Apologies Server runs as a single stateful process that\nmaintains game state in memory.  It cannot be horizontally scaled, and there is\nno option for an external data store.  There is also only limited support for\nauthentication and authorization - basically, any player can register any\navailable handle.  We do enforce resource limits (open connections, registered\nusers, in-progress games) to limit the amount of damage abusive clients can do.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pronovic/apologies-server',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
