# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleantoots', 'cleantoots.commands']

package_data = \
{'': ['*']}

install_requires = \
['Mastodon.py>=1.5.0,<2.0.0',
 'click>=7.0,<8.0',
 'html2text>=2019.9.26,<2020.0.0',
 'pendulum>=2.0.5,<3.0.0']

entry_points = \
{'console_scripts': ['cleantoots = cleantoots.main:cli']}

setup_kwargs = {
    'name': 'cleantoots',
    'version': '0.4.0',
    'description': 'Cleanup your toot history.',
    'long_description': '# Cleantoots\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FCrocmagnon%2Fcleantoots%2Fbadge&style=flat)](https://actions-badge.atrox.dev/Crocmagnon/cleantoots/goto)\n\nCleantoots helps you delete your old toots. Because not everything we say on social medias should stay there for eternity.\n\n## Config\n### Initial setup\nOnly once\n\n```bash\npython -m pip install cleantoots\ncleantoots config setup  # See the following section for config file options\ncleantoots config login\n```\n\n### View and edit\nYou can later view the parsed config file with\n```bash\ncleantoots config list\n```\n\nYou can edit the config file using \n```bash\ncleantoots config edit\n```\n\nThis will open the config file using your preferred editor (`EDITOR` env variable).\n\n## Config options\n\n```ini\n# Any key in this section will serve as a default for other sections\n[DEFAULT]\n\n# Toots that have at least this number of boosts won\'t be deleted.\nboost_limit = 5\n\n# Toots that have at least this number of favorites won\'t be deleted.\nfavorite_limit = 5\n\n# Toots that are more recent than this number of days won\'t be deleted.\ndays_count = 30\n\n# The timezone to use for dates comparisons.\ntimezone = Europe/Paris\n\n# Each section represents an account.\n[Fosstodon]\n# Your Mastodon server URL.\napi_base_url = https://fosstodon.org\n\n# These files are used to store app information obtained when running `login`.\n# The files must be different between accounts. Two different files are required per account.\napp_secret_file = fosstodon_app.secret\nuser_secret_file = fosstodon_user.secret\n\n# IDs of toots you want to protect (never delete).\n# You can find the toot ID in the URL when viewing a toot.\nprotected_toots = 103362008817616000\n    103361883565013391\n    103363106195441418\n\n# Tags you want to protect (never delete).\n# Tags are matched case insensitively and are only matched for original toots (not for boosts):\n# if you boost a toot containing #ScreenshotSunday it won\'t be protected by this rule.\n# You MUST omit the `#` part of the tag.\nprotected_tags = 100DaysToOffload\n    screenshotsunday\n\n\n# Another account\n[Mastodon.social]\napi_base_url = https://mastodon.social\napp_secret_file = mastodonsocial_app.secret\nuser_secret_file = mastodonsocial_user.secret\n\n# Overriding some defaults\nboost_limit = 10\nfavorite_limit = 30\ndays_count = 7\n```\n\n## Run\n\nSee `cleantoots config` for the current config.\n\n```bash\ncleantoots clean  # Defaults to a dry run. Does NOT delete.\ncleantoots clean --delete  # Delete without prompt.\n```\n\n## Add an account\n```bash\ncleantoots config edit  # Opens editor so you can add your config\ncleantoots config list  # Check your newly added account\ncleantoots config login --only-missing  # Store credentials for your newly created account\ncleantoots clean --delete\n```\n\n## Remove an account\n```bash\n# This deletes stored credentials for accounts described in the main config file.\ncleantoots config clear-credentials\n\n# You can then edit the config and remove some accounts:\ncleantoots config edit\n\n# Then login again for remaining accounts.\ncleantoots config login\n```\n\n## Tested environments\nCleantoots test suite runs on Python 3.6, 3.7 and 3.8\non latest versions of macOS, Windows and Ubuntu as GitHub Actions understands it.\n\nSee\n[the docs](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idruns-on)\nfor more information on what "latest" means.\n\n## Inspiration\nThe idea behind cleantoots is highly inspired by [magnusnissel/cleantweets](https://github.com/magnusnissel/cleantweets).\n',
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel@augendre.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Crocmagnon/cleantoots/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
