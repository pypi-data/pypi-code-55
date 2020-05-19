# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delairstack_cli']

package_data = \
{'': ['*'], 'delairstack_cli': ['share/*']}

install_requires = \
['click_spinner==0.1.8',
 'jsonschema==3.2.0',
 'python-delairstack==1.7.7',
 'pyyaml==5.3.1',
 'tabulate==0.8.7',
 'typer[all]==0.1.1']

entry_points = \
{'console_scripts': ['delairstack = delairstack_cli.main:app']}

setup_kwargs = {
    'name': 'delairstack-cli',
    'version': '0.1.1',
    'description': 'CLI for delairstack',
    'long_description': '# CLI for delairstack\n\n# `delairstack`\n\n**Usage**:\n\n```console\n$ delairstack [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell (shell must be restarted after installing it in order to use it).\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `analytics`: Interact with Analytics\n* `configure`: Configure your credentials to connect to the...\n* `products`: Interact with Products\n\n## `delairstack configure`\n\nConfigure your credentials to connect to the platform \n\n**Usage**:\n\n```console\n$ delairstack configure [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `delairstack analytics`\n\nInteract with Analytics\n\n**Usage**:\n\n```console\n$ delairstack analytics [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a new analytic\n* `delete`: Delete an analytic\n* `list`: List the analytics\n\n### `delairstack analytics create`\n\nCreate a new analytic \n\n**Usage**:\n\n```console\n$ delairstack analytics create [OPTIONS]\n```\n\n**Options**:\n\n* `--description PATH`: Path of the Analytic description (YAML file)  [required]\n* `--company TEXT`: Company identifier\n* `--help`: Show this message and exit.\n\n### `delairstack analytics delete`\n\nDelete an analytic \n\n**Usage**:\n\n```console\n$ delairstack analytics delete [OPTIONS] ANALYTIC_NAME\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `delairstack analytics list`\n\nList the analytics \n\n**Usage**:\n\n```console\n$ delairstack analytics list [OPTIONS]\n```\n\n**Options**:\n\n* `--limit INTEGER`: Max number of analytics returned\n* `--help`: Show this message and exit.\n\n## `delairstack products`\n\nInteract with Products\n\n**Usage**:\n\n```console\n$ delairstack products [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `cancel`: Cancel a running product\n* `list`: List the products\n* `logs`: Retrieve the logs of a product\n\n### `delairstack products cancel`\n\nCancel a running product \n\n**Usage**:\n\n```console\n$ delairstack products cancel [OPTIONS] PRODUCT_ID\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `delairstack products list`\n\nList the products \n\n**Usage**:\n\n```console\n$ delairstack products list [OPTIONS]\n```\n\n**Options**:\n\n* `-n, --limit INTEGER`: Max number of analytics returned  [default: 10]\n* `--analytic TEXT`: Analytic name\n* `--company TEXT`: Company identifier\n* `--status [pending|processing|available|rejected|failed]`: Product status\n* `--all`: If set, display also the products from internal analytics (otherwise only products from external analytics are displayed).\n* `--help`: Show this message and exit.\n\n### `delairstack products logs`\n\nRetrieve the logs of a product \n\n**Usage**:\n\n```console\n$ delairstack products logs [OPTIONS] PRODUCT_ID\n```\n\n**Options**:\n\n* `-f, --follow`: Follow logs\n* `--help`: Show this message and exit.\n\n---\n\n*Generated with `typer delairstack_cli/main.py utils docs --name delairstack`*',
    'author': 'delair.ai Backend Team',
    'author_email': 'backend-team@delair.aero',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
