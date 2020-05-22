# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arctic_tern']

package_data = \
{'': ['*']}

extras_require = \
{'asyncpg': ['asyncpg>=0.20.1,<0.21.0'], 'psycopg': ['psycopg2>=2.7,<3.0']}

setup_kwargs = {
    'name': 'arctic-tern',
    'version': '0.2.0',
    'description': 'SQL migrations for python and postgres',
    'long_description': 'Arctic Tern: Simple Postgres migrations for Python\n==================================================\n.. image:: https://travis-ci.org/ConvergysLabs/arctic-tern.svg?branch=master\n    :target: https://travis-ci.org/ConvergysLabs/arctic-tern\n\n.. image:: https://codecov.io/github/ConvergysLabs/arctic-tern/coverage.svg?branch=master\n    :target: https://codecov.io/github/ConvergysLabs/arctic-tern\n    :alt: codecov.io\n\n.. image:: https://upload.wikimedia.org/wikipedia/commons/2/29/2009_07_02_-_Arctic_tern_on_Farne_Islands_-_The_blue_rope_demarcates_the_visitors%27_path.JPG\n    :target: https://en.wikipedia.org/wiki/Arctic_tern\n\nYou can be strongly migratory, too!\n\nFeature Support\n---------------\n\n- Plain SQL update scripts\n- Timestamped update scripts\n- Code-level integration (no CLI needed)\n\nArctic Tern officially supports Python 3.6+\n\nInstallation\n------------\n\nTo install Arctic Tern, simply `pip install arctic-tern`\n\nPublishing\n----------\n    python setup.py sdist bdist\n\n    twine upload --repository-url https://test.pypi.org/legacy/ dist/*\n\n    twine upload dist/arctic_tern-0.1.11.tar.gz\n\nDocumentation\n-------------\n\nDocumentation is good!  We should get some.\n\n\nHow to Contribute\n-----------------\n\nThis would also be good.\n',
    'author': 'Eric Grunzke',
    'author_email': 'eric@grunzke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ConvergysLabs/arctic-tern',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
