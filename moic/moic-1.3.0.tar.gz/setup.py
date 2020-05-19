# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moic',
 'moic.cli',
 'moic.cli.commands',
 'moic.cli.commands.context',
 'moic.cli.commands.issue',
 'moic.cli.commands.rabbit',
 'moic.cli.commands.resources',
 'moic.cli.commands.template',
 'moic.cli.completion',
 'moic.cli.utils',
 'moic.cli.validators',
 'moic.plugins',
 'moic.plugins.jira',
 'moic.plugins.jira.commands',
 'moic.plugins.jira.commands.issue',
 'moic.plugins.jira.commands.resources',
 'moic.plugins.jira.commands.sprint',
 'moic.plugins.jira.completion',
 'moic.plugins.jira.utils',
 'moic.plugins.jira.validators']

package_data = \
{'': ['*']}

install_requires = \
['antidote>=0.7.0,<0.8.0',
 'click>=7.1.1,<8.0.0',
 'commonmark>=0.9.1,<0.10.0',
 'dynaconf>=2.2.3,<3.0.0',
 'jira',
 'keyring>=21.1.1,<22.0.0',
 'pyyaml>=5.3,<6.0',
 'rich>=0.8.8,<0.9.0',
 'tomd>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['moic = moic.base:run']}

setup_kwargs = {
    'name': 'moic',
    'version': '1.3.0',
    'description': 'My Own Issue CLI (Jira, Gitlab etc...)',
    'long_description': '# MOIC : My Own Issue CLI\n\n> Freely inspired by https://pypi.org/project/jira-cli/\n\nCommand line utility to interact with issue manager such as Jira\n\n## Getting Started\n\n* Install moic\n```bash\n> pip install moic\n```\n\n* Configure moic\n```bash\n> moic configure\n```\n\n* Commands\n```bash\n> moic\nUsage: moic [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  config    Configure Jira cli, setting up instance, credentials etc...\n  issue     Create, edit, list Jira issues\n  list      List projects, issue_types, priorities, status\n  rabbit    Print an amazing rabbit: Tribute to @fattibenji...\n  sprint    Create, edit, list Jira Sprints\n  template  List, edit templates\n  version   Provide the current moic installed version\n```\n\n## Autocompletion\n\nTo activate bash autocompletion just add:\n* For bash\n```\n# In your .bashrc\neval "$(_MOIC_COMPLETE=source_bash moic)"\n```\n* For zsh\n```\n# In your .zshrc\neval "$(_MOIC_COMPLETE=source_zsh moic)"\n```\n\n## Contribute\n\nFeel free [open issues on Gitlab](https://gitlab.com/brice.santus/moic/-/issues) or propose Merge Requests\n\n### Prerequisites\n\nThis project is based on [Poetry](https://python-poetry.org/docs/) as a package manager. It allows the use of virtual environments and the lock of package versions, whether they are in your dependencies or just sub-dependencies of these dependencies.\n\n### Setup\n\n* Create virtualenv (Optionnaly you can use [pyenv](https://github.com/pyenv/pyenv) which is a Python Virtualenv Manager in combination with **Poetry**)\n```bash\npoetry shell\n```\n* Install dependencies\n```bash\npoetry install\n```\n* Install pre-commit (using [Pre-commit framework](https://pre-commit.com/))\n```bash\npre-commit install\n```\n> Pre-commit will check isort, black, flake8\n\n###\xa0Commit messages\n\nThis project uses semantic versioning so it is important to follow the rules of [conventional commits](https://www.conventionalcommits.org/).\n',
    'author': 'Brice Santus',
    'author_email': 'brice.santus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/brice.santus/moic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
