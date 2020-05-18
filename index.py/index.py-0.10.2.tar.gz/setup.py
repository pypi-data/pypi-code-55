# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indexpy', 'indexpy.http', 'indexpy.openapi', 'indexpy.websocket']

package_data = \
{'': ['*']}

install_requires = \
['a2wsgi>=0.3.4,<0.4.0',
 'aiofiles>=0.5.0,<0.6.0',
 'gunicorn>=20.0.4,<21.0.0',
 'jinja2>=2.10.3,<3.0.0',
 'pydantic>=1.5,<2.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.3,<6.0',
 'starlette>=0.13.1,<0.14.0',
 'uvicorn>=0.11.3,<0.12.0',
 'watchdog>=0.10.2,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0'],
 'test': ['requests>=2.23.0,<3.0.0', 'pytest>=5.4.2,<6.0.0']}

entry_points = \
{'console_scripts': ['index-cli = indexpy.cli:main']}

setup_kwargs = {
    'name': 'index.py',
    'version': '0.10.2',
    'description': 'An easy-to-use asynchronous web framework based on ASGI.',
    'long_description': None,
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/index.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
