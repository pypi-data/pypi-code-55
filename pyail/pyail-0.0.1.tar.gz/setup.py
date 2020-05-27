# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyail']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pyail',
    'version': '0.0.1',
    'description': '',
    'long_description': 'PyAIL\n======\n\n[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)\n\n# PyAIL - Python library using the AIL Rest API\n\nPyMISP is a Python library to access [AIL](https://github.com/ail-project/ail-framework) platforms via their REST API.\n\n## Install from pip\n\n**It is strongly recommended to use a virtual environment**\n\nIf you want to know more about virtual environments, [python has you covered](https://docs.python.org/3/tutorial/venv.html)\n\nInstall pyail:\n```bash\npip3 install pyail\n```\n',
    'author': 'Aurelien Thirion (terrtia)',
    'author_email': 'aurelien.thirion@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ail-project/PyAIL',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
