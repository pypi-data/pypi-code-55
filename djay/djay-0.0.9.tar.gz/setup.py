# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djay',
 'djay.blueprints',
 'djay.blueprints.command',
 'djay.blueprints.init',
 'djay.blueprints.model',
 'djay.commands',
 'djay.utils']

package_data = \
{'': ['*'],
 'djay.blueprints.command': ['templates/{{app}}/*',
                             'templates/{{app}}/management/*',
                             'templates/{{app}}/management/commands/*'],
 'djay.blueprints.init': ['templates/*',
                          'templates/tests/*',
                          'templates/{{app}}/*',
                          'templates/{{app}}/management/*',
                          'templates/{{app}}/management/commands/*',
                          'templates/{{app}}/migrations/*',
                          'templates/{{app}}/models/*',
                          'templates/{{app}}/utils/*'],
 'djay.blueprints.model': ['templates/tests/*',
                           'templates/tests/unit/*',
                           'templates/tests/unit/models/*',
                           'templates/{{app}}/models/*']}

install_requires = \
['click', 'flake8', 'inflection', 'jinja2', 'pyyaml', 'redbaron', 'six']

setup_kwargs = {
    'name': 'djay',
    'version': '0.0.9',
    'description': 'The advanced Django CLI',
    'long_description': None,
    'author': 'aleontiev',
    'author_email': 'alonetiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
