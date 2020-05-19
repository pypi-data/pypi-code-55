# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_time_report']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'python-gitlab>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'gitlab-time-report',
    'version': '0.1.dev3',
    'description': 'GitLab time reporting made easy.',
    'long_description': '# GitLab-time-report\n\nPlease visit the [Read the Docs](http://ifs.pages.ifs.hsr.ch/gitlab-time-report/gitlab-time-report/) documentation for more information.\n\n## Development\n\nPlease visit the [according documentation page](http://ifs.pages.ifs.hsr.ch/gitlab-time-report/gitlab-time-report/development/).\n',
    'author': 'Johannes Wildermuth',
    'author_email': 'johannes.wildermuth@hsr.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.dev.ifs.hsr.ch/ifs/gitlab-time-report/gitlab-time-report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
