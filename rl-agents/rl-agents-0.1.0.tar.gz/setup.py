# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rl_agents']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rl-agents',
    'version': '0.1.0',
    'description': 'Implementation of various reinforcement learning methods.',
    'long_description': "=========\nRL-Agents\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/rl-agents.svg\n        :target: https://pypi.python.org/pypi/rl-agents\n\n.. image:: https://img.shields.io/travis/mateuspontesm/rl-agents.svg\n        :target: https://travis-ci.org/mateuspontesm/rl-agents\n\n.. image:: https://readthedocs.org/projects/rl-agents/badge/?version=latest\n        :target: https://rl-agents.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nImplementation of various reinforcement learning methods.\n\n\n* Free software: BSD 3-Clause 'New' or 'Revised' License\n\n* Documentation: https://rl-agents.readthedocs.io.\n\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `mateuspontesm/cookiecutter-poetry`_ project template,\na fork of `johanvergeer/cookiecutter-poetry`_ project template\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`johanvergeer/cookiecutter-poetry`: https://github.com/johanvergeer/cookiecutter-poetry\n.. _`mateuspontesm/cookiecutter-poetry`: https://github.com/mateuspontesm/cookiecutter-poetry\n",
    'author': 'Mateus Mota',
    'author_email': 'mateuspontesm@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mateuspontesm/rl-agents',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
