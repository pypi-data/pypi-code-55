# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_stories',
 '_stories.contrib',
 '_stories.contrib.debug_toolbars',
 '_stories.contrib.debug_toolbars.django',
 '_stories.contrib.debug_toolbars.flask',
 '_stories.execute',
 'stories',
 'stories.contrib',
 'stories.contrib.debug_toolbars',
 'stories.contrib.sentry']

package_data = \
{'': ['*'],
 '_stories.contrib.debug_toolbars.django': ['templates/stories/debug_toolbar/*'],
 '_stories.contrib.debug_toolbars.flask': ['templates/stories/debug_toolbar/*']}

entry_points = \
{'pytest11': ['stories = stories.contrib.pytest']}

setup_kwargs = {
    'name': 'stories',
    'version': '1.0.0',
    'description': 'Define a user story in the business transaction DSL',
    'long_description': '![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png)\n\n[![azure-devops-builds](https://img.shields.io/azure-devops/build/dry-python/stories/3?style=flat-square)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)\n[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/dry-python/stories/3?style=flat-square)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)\n[![readthedocs](https://img.shields.io/readthedocs/stories?style=flat-square)](https://stories.readthedocs.io/en/latest/?badge=latest)\n[![gitter](https://img.shields.io/gitter/room/dry-python/stories?style=flat-square)](https://gitter.im/dry-python/stories)\n[![pypi](https://img.shields.io/pypi/v/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)\n\n---\n\n# The business transaction DSL\n\n- [Source Code](https://github.com/dry-python/stories)\n- [Issue Tracker](https://github.com/dry-python/stories/issues)\n- [Documentation](https://stories.readthedocs.io/en/latest/)\n- [Newsletter](https://twitter.com/dry_py)\n- [Discussion](https://gitter.im/dry-python/stories)\n\n## Installation\n\nAll released versions are hosted on the Python Package Index. You can\ninstall this package with following command.\n\n```bash\npip install stories\n```\n\n## Usage\n\n`stories` provide a simple way to define a complex business scenario\nthat include many processing steps.\n\n```pycon\n\n>>> from stories import story, arguments, Success, Failure, Result\n>>> from app.repositories import load_category, load_profile, create_subscription\n\n>>> class Subscribe:\n...\n...     @story\n...     @arguments(\'category_id\', \'profile_id\')\n...     def buy(I):\n...\n...         I.find_category\n...         I.find_profile\n...         I.check_balance\n...         I.persist_subscription\n...         I.show_subscription\n...\n...     def find_category(self, ctx):\n...\n...         ctx.category = load_category(ctx.category_id)\n...         return Success()\n...\n...     def find_profile(self, ctx):\n...\n...         ctx.profile = load_profile(ctx.profile_id)\n...         return Success()\n...\n...     def check_balance(self, ctx):\n...\n...         if ctx.category.cost < ctx.profile.balance:\n...             return Success()\n...         else:\n...             return Failure()\n...\n...     def persist_subscription(self, ctx):\n...\n...         ctx.subscription = create_subscription(category=ctx.category, profile=ctx.profile)\n...         return Success()\n...\n...     def show_subscription(self, ctx):\n...\n...         return Result(ctx.subscription)\n\n>>> Subscribe().buy(category_id=1, profile_id=1)\nSubscription(primary_key=8)\n\n```\n\nThis code style allow you clearly separate actual business scenario from\nimplementation details.\n\n## License\n\nStories library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐️ &mdash;</p>\n<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>\n<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dry-python.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
