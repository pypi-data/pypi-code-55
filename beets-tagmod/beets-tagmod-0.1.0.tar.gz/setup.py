# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beetsplug', 'beetsplug.tagmod']

package_data = \
{'': ['*'], 'beetsplug.tagmod': ['command/*']}

install_requires = \
['beets>=1.4,<2.0', 'confuse>=1.0,<2.0']

setup_kwargs = {
    'name': 'beets-tagmod',
    'version': '0.1.0',
    'description': 'A plugin for beets to modify media tags before they become written.',
    'long_description': '',
    'author': 'Thore Weilbier',
    'author_email': 'thore@weilbier.net',
    'url': 'https://github.com/weilbith/beets-tagmod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
