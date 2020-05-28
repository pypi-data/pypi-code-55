# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['swt']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9.7,<4.0.0']

setup_kwargs = {
    'name': 'swt',
    'version': '0.1.0',
    'description': 'Simple Web Token library for Python',
    'long_description': '# Python SWT Library\n\nPython library for handling `Simple Web Tokens`.\n\n## Caveats\n\n- Please use `pycryptodome` and not `pycrypto` as the later is unmaintained and\n  broken on python 3.8+\n- Currently only supports RSA-SHA256\n\n## TODO\n\n- Add docs\n- Add support HMAC SHA256\n',
    'author': 'David Jack Wange Olrik',
    'author_email': 'david@olrik.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidolrik/python-swt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
