# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smtp4dev']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'smtp4dev',
    'version': '0.1.4',
    'description': 'Provides access to emails caught by the SMTP4dev development server',
    'long_description': '# SMTP4DEV\n\nAn abstraction library to access the messages captured by an\n[SMTP4dev](https://github.com/rnwood/smtp4dev/) instance.\n\n\n## Installation\n\nInstall with pip:\n\n```\npip install smtp4dev\n```\n\n## Usage\n\nExample usage:\n\n```py\nfrom smtp4dev import Smtp4Dev\nclient = Smtp4Dev(\'http://localhost:8080\')\nmessages = client.list_messages()\nemail = client.get_message(next(messages))\nprint(email)\n"[From: romeo@email.com To: juliet@email.com Subject: Meeting Friday night]"\n```\n',
    'author': 'Guillaume Pasquet',
    'author_email': 'guillaume.pasquet@plentific.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
