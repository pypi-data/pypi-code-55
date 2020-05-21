# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_quill', 'sanic_quill.fields', 'sanic_quill.widgets']

package_data = \
{'': ['*'], 'sanic_quill': ['static/editor/*', 'static/tabs/*', 'templates/*']}

install_requires = \
['Sanic-Jinja2>=0.8.0,<0.9.0', 'wtforms>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'sanic-quill',
    'version': '0.0.1',
    'description': 'Sanic-quill is a port of Flask-quill to Sanic ecosystem. (wtforms widget for quill.js editor)',
    'long_description': 'sanic-quill\n-----------\n\nSanic-quill is a port of Flask-quill (https://github.com/drewdru/flask-quill/) to Sanic ecosystem. (wtforms widget for quill.js editor (https://github.com/quilljs/quill))\n\nQuill.js is a modern WYSIWYG editor built for compatibility and extensibility.\n\n',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
