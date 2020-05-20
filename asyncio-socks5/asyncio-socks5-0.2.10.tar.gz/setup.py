# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['socks5', 'socks5.client', 'socks5.server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncio-socks5',
    'version': '0.2.10',
    'description': 'Socks5 Server/Client by asyncio.',
    'long_description': '# Socks5\n\nSocks5 Server/Client by asyncio.\n\n## Reference link:\n\n* [RFC1928](https://www.ietf.org/rfc/rfc1928.txt)\n* [RFC1929](https://www.ietf.org/rfc/rfc1929.txt)\n* [Socks5协议](https://abersheeran.com/articles/Socks5/)\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/socks5',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
