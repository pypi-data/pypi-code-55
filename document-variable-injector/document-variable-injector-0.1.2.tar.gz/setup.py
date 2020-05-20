# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['injector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'document-variable-injector',
    'version': '0.1.2',
    'description': 'Provides method for dynamically injecting variables into a document and/or HTML like object',
    'long_description': "# Document argument injector\n\nProvides a simple helper method\n\nArgument(s):\n- document      (str)   the document loaded as a string\n- params        (dict)  key,value == match,replacement\n- encapsulation (tuple)   variable encapsulation ('leftisde', 'rightside')\n\nReturns the provided document with injected parameters\n\n## Usage\n\n```py\nfrom injector import injector\n\ndocument: str\nwith open('profile.html', 'r') as file:\n    document = file.read()\n\npayload: dict = {\n    'user.firstName': 'John',\n    'user.lastName': 'Smith',\n    'user.email': 'jsmith@example.com',\n    'user.phone': '+555111444'\n    'user.postcode': '1234 Town',\n    'user.address': '12 Street'\n}\n\ninjector(\n    document=document,\n    params=params,\n    encapsulation=('{', '}')\n)\n```",
    'author': 'Alex Pedersen',
    'author_email': 'me@alexpdr.dev',
    'maintainer': 'Alex Pedersen',
    'maintainer_email': 'me@alexpdr.dev',
    'url': 'https://github.com/alexpdr/document-variable-injector',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
