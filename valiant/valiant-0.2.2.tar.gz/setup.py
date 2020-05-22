# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['valiant',
 'valiant.config',
 'valiant.config.source',
 'valiant.console',
 'valiant.console.commands',
 'valiant.console.config',
 'valiant.log',
 'valiant.package',
 'valiant.plugins',
 'valiant.plugins.reports',
 'valiant.plugins.reports.basic',
 'valiant.plugins.reports.safety',
 'valiant.plugins.reports.spdx',
 'valiant.reports',
 'valiant.repositories',
 'valiant.repositories.pypi',
 'valiant.util']

package_data = \
{'': ['*'], 'valiant': ['third-party/hypermodern-python/*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'cleo>=0.7.6,<0.8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow-dataclass>=7.5.2,<8.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.23.0,<3.0.0',
 'safety>=1.8.7,<2.0.0',
 'setuptools>=46.0.0,<47.0.0',
 'structlog>=20.1.0,<21.0.0',
 'texttable>=1.6.2,<2.0.0',
 'wcwidth>=0.1.8,<0.2.0']

entry_points = \
{'console_scripts': ['valiant = valiant.console:main'],
 'valiant.report': ['basic = valiant.plugins.reports.basic:BasicReportPlugin',
                    'demo = valiant.plugins.reports.demo:DemoReportPlugin',
                    'safety = '
                    'valiant.plugins.reports.safety:SafetyReportPlugin',
                    'spdx = '
                    'valiant.plugins.reports.spdx:SpdxLicenseReportPlugin']}

setup_kwargs = {
    'name': 'valiant',
    'version': '0.2.2',
    'description': 'Audit tool to help investigate Python dependencies',
    'long_description': '# Valiant\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Default CI workflow](https://github.com/pomes/valiant/workflows/Default%20CI%20workflow/badge.svg)](https://github.com/pomes/valiant/actions?query=workflow%3A%22Default+CI+workflow%22)\n\nThe Valiant project aims to provide auditing tools that help project teams\ntrack their dependencies in terms of licensing, security, and dependability.\n\nThe goal is to help reduce the fragility of the "input side" of software development\nby making it easy to assess and track dependencies. Further work will also aim to\ncheck dependencies against policy documents to help integrate Valiant into developer\nand release workflows.\n\nThe system is written in Python 3 and targets Python codebases.\n\nPlease check out the [project site](http://pomes.github.io/valiant)\nfor documentation.\n\n## Key resources\n\n| Resource | Description |\n| -------- | ----------- |\n| [Codebase](https://github.com/pomes/valiant) | GitHub project |\n| [Security policy](https://github.com/pomes/valiant/blob/master/SECURITY.md) | Please refer to this if you need to report a security concern |\n| [Project tracker](https://github.com/pomes/valiant/projects/1) | Structured to provide fulfilment of [project milestones](https://github.com/pomes/valiant/milestones) |\n| [Issue tracker](https://github.com/pomes/valiant/issues) | GitHub issues |\n| [Documentation](http://pomes.github.io/valiant) | Project site |\n| [License](https://github.com/pomes/valiant/blob/master/LICENSE) | Project licence (MIT) |\n| [Contributing](https://github.com/pomes/valiant/blob/master/CONTRIBUTING.md) | Want to join in? |\n\n## Attribution\n\nI have used the [Poetry](https://github.com/python-poetry/poetry) library to package\nthis project and guide my implementation efforts.\n\nThe [Hypermodern Python series](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) by\nClaudio Jolowicz is a great resource and you\'ll see his guidance instilled in this codebase.\n\n[ ~ Dependencies scanned by PyUp.io ~ ]\n',
    'author': 'Duncan Dickinson',
    'author_email': 'dedickinson@users.noreply.github.com',
    'maintainer': 'Duncan Dickinson',
    'maintainer_email': 'dedickinson@users.noreply.github.com',
    'url': 'https://github.com/pomes/valiant',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
