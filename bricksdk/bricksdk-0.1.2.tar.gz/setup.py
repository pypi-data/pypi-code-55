# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bricksdk',
 'bricksdk.brick_commands',
 'bricksdk.brick_commands.templates.generic',
 'bricksdk.brick_commands.templates.generic.brick',
 'bricksdk.brick_commands.templates.input',
 'bricksdk.brick_commands.templates.input.brick',
 'bricksdk.brick_processors',
 'bricksdk.configurations',
 'bricksdk.configurations.configuration_detector',
 'bricksdk.configurations.configuration_loader',
 'bricksdk.configurations.configuration_validator',
 'bricksdk.connectors',
 'bricksdk.connectors.grpc',
 'bricksdk.connectors.grpc.proto_processor',
 'bricksdk.observer',
 'bricksdk.proto_store',
 'bricksdk.solution_runner',
 'bricksdk.solution_runner.brick_runner']

package_data = \
{'': ['*'],
 'bricksdk.brick_commands.templates.generic': ['configurations/*', 'protos/*'],
 'bricksdk.brick_commands.templates.input': ['configurations/*', 'protos/*'],
 'bricksdk.proto_store': ['protos/*']}

install_requires = \
['grpcio', 'grpcio-tools']

setup_kwargs = {
    'name': 'bricksdk',
    'version': '0.1.2',
    'description': 'SDK to create plugable bricks in lumoz.ai',
    'long_description': None,
    'author': 'Attinad Software',
    'author_email': 'attinad@attinadsoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<3.6',
}


setup(**setup_kwargs)
