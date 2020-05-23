# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cp_template']
install_requires = \
['coleo>=0.1.3,<0.2.0', 'pystache>=0.5.4,<0.6.0']

entry_points = \
{'console_scripts': ['cp-template = cp_template:main']}

setup_kwargs = {
    'name': 'cp-template',
    'version': '0.1.0',
    'description': 'A tool to copy templated directories',
    'long_description': '\n# cp-template\n\n\nThis is a very simple utility to generate directories based on templates.\n\n\n## Install\n\n\n```bash\npip install cp-template\n```\n\n\n## Usage\n\n\nSuppose you have the following directory structure (**Note: the {{}}s are part of the filenames**)\n\n```\n{{project}}/\n  .gitignore\n  README.md        # File contains "{{project}} by {{author}}"\n  {{project}}/\n    __init__.py\n```\n\nThen you can run the following command:\n\n```\ncp-template \'./{{project}}\' project=pineapple author=me\n```\n\nAnd it will generate this in the current directory:\n\n```\npineapple/\n  .gitignore\n  README.md        # File contains "pineapple by me"\n  pineapple/\n    __init__.py\n```\n\nMore features will be added as I need them, but feel free to make PRs to contribute some.\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/cp-template',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
