# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keydope']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.3,<2.0',
 'inotify_simple>=1.3,<2.0',
 'python-xlib>=0.27,<0.28',
 'pyyaml>=5.3,<6.0']

extras_require = \
{'systemd': ['sdnotify>=0.3,<0.4', 'dbus-python>=1.2,<2.0']}

setup_kwargs = {
    'name': 'keydope',
    'version': '0.2.0a2',
    'description': '',
    'long_description': '# Keydope\n\nKeydope is a flexible keyboard remapping tool written in Python, originally\nforked from [xkeysnail](https://github.com/mooz/xkeysnail).\nIt currently only supports Linux, but support for Windows is planned.\n\nIt can replace tools such as xmodmap, xbindkeys, sxhkd, xchainkeys, and xcape.\n',
    'author': 'infokiller',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/infokiller/keydope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
