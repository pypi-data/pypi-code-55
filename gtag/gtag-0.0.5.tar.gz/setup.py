# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtag']

package_data = \
{'': ['*']}

install_requires = \
['guy>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'gtag',
    'version': '0.0.5',
    'description': 'GUI Lib for python3 (depends on guy), components based',
    'long_description': '# gtag\n\nA [guy](https://github.com/manatlan/guy) sub module ;-)\n\n[Official docs](https://gtag-docs.glitch.me/)\n\nBefore prime time version:\n\n* permit to return js (in gtag or tag)\n* refacto a little bit\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manatlan/guy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
