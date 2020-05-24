# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_primitive_cli', 'slack_primitive_cli.command']

package_data = \
{'': ['*']}

install_requires = \
['click-option-group', 'click>=7,<8', 'slackclient>=2.6,<3.0']

entry_points = \
{'console_scripts': ['slackcli = slack_primitive_cli.__main__:cli']}

setup_kwargs = {
    'name': 'slack-primitive-cli',
    'version': '0.1.2',
    'description': 'Primitive Slack CLI',
    'long_description': '# slack-primitive-cli\n[![Build Status](https://travis-ci.org/yuji38kwmt/slack-primitive-cli.svg?branch=master)](https://travis-ci.org/yuji38kwmt/slack-primitive-cli)\n[![PyPI version](https://badge.fury.io/py/slack-primitive-cli.svg)](https://badge.fury.io/py/slack-primitive-cli)\n[![Python Versions](https://img.shields.io/pypi/pyversions/slack-primitive-cli.svg)](https://pypi.org/project/slack-primitive-cli/)\n\n`slack-primitive-cli` can execute [Slack web api methods](https://api.slack.com/methods) from command line.\nCommand line argument is correspont to web api arguments, so `slack-primitive-cli` is **primitive**.\n\n\n# Requirements\n* Python 3.6+\n\n# Install\n\n```\n$ pip install slack-primitive-cli\n```\n\nhttps://pypi.org/project/slack-primitive-cli/\n\n\n# Usage\n\n## Sending a message\n\n```\n$ slackcli chat.postMessage --token xoxb-XXXXXXX --channel "#random" --text hello\n\n$ export SLACK_API_TOKEN=xoxb-XXXXXXX\n$ slackcli chat.postMessage  --channel "#random" --text hello\n```\n\n## Uploading files\n\n```\n$ slackcli files.upload --channels "#random" --file foo.txt\n```\n\n\n# Supported web api methods.\n`slack-primitive-cli` supports a few web api methods.\n\n* [chat.delete](https://api.slack.com/methods/chat.delete)\n* [chat.postMessage](https://api.slack.com/methods/chat.postMessage)\n* [files.delete](https://api.slack.com/methods/files.delete)\n* [files.upload](https://api.slack.com/methods/files.upload)\n\n# Additional\n\n## Shell Completion\n`slack-primitive-cli` depends on [click](https://click.palletsprojects.com/en/7.x/), so `slack-primitive-cli` can provide tab completion.\nBash, Zsh, and Fish are supported\n\nIn order to activate shell completion, you need to execute the following script.\n\n```\n$ eval "$(_SLACKCLI_COMPLETE=source slackcli)"\n```\n\n\nSee [here](https://click.palletsprojects.com/en/7.x/bashcomplete/) for details.\n\n',
    'author': 'yuji38kwmt',
    'author_email': 'yuji38kwmt@gmail.com',
    'maintainer': 'yuji38kwmt',
    'maintainer_email': 'yuji38kwmt@gmail.com',
    'url': 'https://github.com/yuji38kwmt/slack-primitive-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
