# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_dependencies', '_dependencies.checks', 'dependencies']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dependencies',
    'version': '2.0.0',
    'description': 'Dependency Injection for Humans',
    'long_description': '![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)\n\n[![azure-devops-builds](https://img.shields.io/azure-devops/build/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)\n[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)\n[![readthedocs](https://img.shields.io/readthedocs/dependencies?style=flat-square)](https://dependencies.readthedocs.io/en/latest/?badge=latest)\n[![gitter](https://img.shields.io/gitter/room/dry-python/dependencies?style=flat-square)](https://gitter.im/dry-python/dependencies)\n[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.python.org/pypi/dependencies/)\n[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)\n\n---\n\n# Dependency Injection for Humans\n\n- [Source Code](https://github.com/dry-python/dependencies)\n- [Issue Tracker](https://github.com/dry-python/dependencies/issues)\n- [Documentation](https://dependencies.readthedocs.io/en/latest/)\n- [Newsletter](https://twitter.com/dry_py)\n- [Discussion](https://gitter.im/dry-python/dependencies)\n\n## Installation\n\nAll released versions are hosted on the Python Package Index. You can\ninstall this package with following command.\n\n```bash\npip install dependencies\n```\n\n## Usage\n\nDependency injection without `dependencies`\n\n```pycon\n\n>>> from app.robot import Robot, Servo, Amplifier, Controller, Settings\n\n>>> robot = Robot(\n...     servo=Servo(amplifier=Amplifier()),\n...     controller=Controller(),\n...     settings=Settings(environment="production"),\n... )\n\n>>> robot.work()\n\n```\n\nDependency injection with `dependencies`\n\n```pycon\n\n>>> from dependencies import Injector\n\n>>> class Container(Injector):\n...     robot = Robot\n...     servo = Servo\n...     amplifier = Amplifier\n...     controller = Controller\n...     settings = Settings\n...     environment = "production"\n\n>>> Container.robot.work()\n\n```\n\n## License\n\nDependencies library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐️ &mdash;</p>\n<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>\n<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dry-python.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
