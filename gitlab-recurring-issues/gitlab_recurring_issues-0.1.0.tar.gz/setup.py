# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_recurring_issues']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.0,<3.0.0', 'python-gitlab>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['recurring_issues = gitlab_recurring_issues.main:main']}

setup_kwargs = {
    'name': 'gitlab-recurring-issues',
    'version': '0.1.0',
    'description': 'Gitlab Bot to automatically (re)create recurring issues in project',
    'long_description': None,
    'author': 'Thomas Chiroux',
    'author_email': 'thomas@chiroux.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
