# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rename_movie']
install_requires = \
['isle>=0.6.0,<0.7.0', 'macos-tags>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['rename-movie = rename_movie:main',
                     'rnmv = rename_movie:main']}

setup_kwargs = {
    'name': 'rename-movie',
    'version': '1.1.0',
    'description': 'Rename and organize movies',
    'long_description': 'A script renames the movie file, tags it with genres, and moves\nto the folder with the director’s name.\n',
    'author': 'Dima Koskin',
    'author_email': 'dmksknn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
