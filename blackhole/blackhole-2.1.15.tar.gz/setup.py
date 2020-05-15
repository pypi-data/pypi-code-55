# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackhole']

package_data = \
{'': ['*']}

install_requires = \
['coverage[dev,tests]>=5.1,<6.0',
 'guzzle_sphinx_theme[dev,docs]>=0.7.11,<0.8.0',
 'pre-commit[dev]>=2.4.0,<3.0.0',
 'pytest-asyncio[dev,tests]>=0.12.0,<0.13.0',
 'pytest-clarity[dev,tests]>=0.3.0-alpha.0,<0.4.0',
 'pytest-cov[dev,tests]>=2.8.1,<3.0.0',
 'pytest[dev,tests]>=5.4.2,<6.0.0',
 'setproctitle[setproctitle]>=1.1.10,<2.0.0',
 'sphinx[dev,docs]>=3.0.3,<4.0.0',
 'tox[dev]>=3.15.0,<4.0.0',
 'uvloop[uvloop]>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['blackhole = blackhole.application:run',
                     'blackhole_config = '
                     'blackhole.application:blackhole_config']}

setup_kwargs = {
    'name': 'blackhole',
    'version': '2.1.15',
    'description': 'Blackhole is an MTA (message transfer agent) that (figuratively) pipes all mail to /dev/null.',
    'long_description': "=========\nBlackhole\n=========\n\n.. image:: https://img.shields.io/travis/kura/blackhole/master.svg?style=for-the-badge&label=tests\n    :target: http://travis-ci.org/kura/blackhole\n    :alt: Build status of the master branch\n\n.. image:: https://img.shields.io/codecov/c/github/kura/blackhole/master.svg?style=for-the-badge&label=coverage\n    :target: https://codecov.io/github/kura/blackhole/\n    :alt: Test coverage\n\n.. image:: https://img.shields.io/codacy/grade/fa797b3c1c18495aa2331d327c04bb9c.svg?style=for-the-badge\n    :target: https://www.codacy.com/app/kura/blackhole/dashboard\n    :alt: Codacy grade\n\n.. image:: https://img.shields.io/requires/github/kura/blackhole.svg?style=for-the-badge\n    :target: https://requires.io/github/kura/blackhole/requirements/?branch=master\n    :alt: Requirements Status\n\nBlackhole is an `MTA (message transfer agent)\n<https://en.wikipedia.org/wiki/Message_transfer_agent>`_ that (figuratively)\npipes all mail to /dev/null, built on top of `asyncio\n<https://docs.python.org/3/library/asyncio.html>`_ and utilises `async def <https://docs.python.org/3/reference/compound_stmts.html#async-def>`_\nand `await\n<https://docs.python.org/3/reference/expressions.html#await>`_ statements\navailable in `Python 3.5 <https://docs.python.org/3/whatsnew/3.5.html>`_.\n\nWhile Blackhole is an MTA, none of the actions performed via SMTP or SMTPS are\nactually processed, and no email is delivered. You can tell Blackhole how to\nhandle mail that it receives. It can accept all of it, bounce it all, or\nrandomly do either of those two actions.\n\nThink of Blackhole sort of like a honeypot in terms of how it handles mail, but\nit's specifically designed with testing in mind.\n\n\nDocumentation\n=============\n\nYou can find the latest documentation `here\n<https://kura.github.io/blackhole/>`_.\n\nIf you would like to contribute, please read the `contributors guide\n<https://kura.github.io/blackhole/overview.html#contributing>`_.\n\nThe latest build status on `travis <https://travis-ci.org/kura/blackhole/>`_.\n\nAnd the test coverage report on `codecov\n<https://codecov.io/github/kura/blackhole/>`_.\n\nChangelog\n=========\n\nYou can find a list of changes `on the\nblackhole website <https://kura.github.io/blackhole/changelog.html>`_.\n",
    'author': 'Kura',
    'author_email': 'kura@kura.gg',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kura.github.io/blackhole/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6.1,<4',
}


setup(**setup_kwargs)
