# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fn_deps']
install_requires = \
['click>=7.1.2,<8.0.0',
 'dephell>=0.8.3,<0.9.0',
 'gitpython>=3.1.2,<4.0.0',
 'sh>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['fn_deps = fn_deps:cli']}

setup_kwargs = {
    'name': 'fn-deps',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Fn Deps\n\nSimple helpers for managing and publishing dependencies.\n\nThis is used by teh fn_graph project and currently only supports poetry based repos. The primary point is to make publishing a package easy and dependable. The main call is:\n\n`fn_deps publish <major|minor|patch>`\n\nThis will:\n\n* Check there are no uncommitted changed\n* Check you are up to date with the origin/master branch\n* Update the package version\n* Use dephell to create a setup.py (very nice for local development)\n* Commit the changes ot the version and setup.py\n* Build the package\n* Tag the commit with the version\n* Push the branch and the tags to origin\n* Publish the package on Pypi\n\nIf anything goes wrong it will revert to the original commit without any changes.\n',
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BusinessOptics/fn_deps',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
