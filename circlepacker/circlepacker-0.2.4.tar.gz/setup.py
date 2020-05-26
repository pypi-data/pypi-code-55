# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['circlepacker',
 'circlepacker.domain',
 'circlepacker.optimization',
 'circlepacker.routers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.54.2,<0.55.0',
 'pydantic>=1.5.1,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'uvicorn>=0.11.5,<0.12.0']

setup_kwargs = {
    'name': 'circlepacker',
    'version': '0.2.4',
    'description': 'A service for computing circle packing',
    'long_description': '# Circle Packer\n<img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/osullivryan/circle-packer/Release Master Branch?style=flat-square"> <img alt="PyPi Version" src="https://img.shields.io/pypi/v/circlepacker?style=flat-square">\n\n\n## Why pack circles?\n\nSticking circles as close together as possible!\n\n## How to use\n\nCurrently it is only through the API. You can install it using pip:\n\n```pip install circlepacker```\n\nAnd then run the service using:\n\n```python -m circlepacker```\n\nFollowing the link provided and routing to `/docs` will get you to the Swagger documentation where you can try it out.\n\n![API](resources/docs.png)\n\n## TODO\n\n* Finalize backend routing to include better pydantic typing for contracts.\n* Create simple frontend \n* Deploy to AWS services',
    'author': "Ryan O'Sullivan",
    'author_email': 'osullivryan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/osullivryan/circle-packer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
