# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_ci_updater', 'poetry_ci_updater.providers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'gitpython>=3.0.0,<4.0.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['poetry-ci-updater = poetry_ci_updater.main:main']}

setup_kwargs = {
    'name': 'poetry-ci-updater',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Poetry CI Updater\n\nThis package is intended to help integrating poetry with your CI.\n\nIt will create a new branch where it will push the updated poetry.lock to.\nIf your git provider is supported, it will also create a pull/merge request.\n\n## Installation\n### Pypi\n```yaml\npoetry add --dev poetry-ci-updater\n```\n\n### Git\n```shell\npoetry add --dev git+https://github.com/MarcoGlauser/poetry-ci-updater@master\n```\n\n\n## Usage\n### Gitlab\nBecause Gitlab currently can\'t write to the repository with the $CI_JOB_TOKEN, you will need \nto define a secret enviroment variable  with the name PERSONAL_ACCESS_TOKEN.\n```yaml\nupdate-dependencies:\n  stage: build\n  image: python:3.8\n  before_script:\n    - git config user.email "{$GITLAB_USER_EMAIL}"\n    - git config user.name "${GITLAB_USER_NAME}"\n  script:\n    - pip install poetry\n    - git remote rm origin\n    - git remote add origin https://gitlab-ci-token:${PERSONAL_ACCESS_TOKEN}@${CI_SERVER_HOST}:${CI_SERVER_PORT}/${CI_PROJECT_PATH}.git\n    - CI_JOB_TOKEN=${PERSONAL_ACCESS_TOKEN} poetry run poetry-ci-updater\n  rules:\n    - if: $CI_PIPELINE_SOURCE == "schedule"\n```\n\n## TODO\n* Github Actions support\n* Tests\n* Provider Options\n* Keep update branch up to date',
    'author': 'MarcoGlauser',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarcoGlauser/poetry-ci-updater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
