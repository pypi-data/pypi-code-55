# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azulejo']

package_data = \
{'': ['*'], 'azulejo': ['bin/*']}

install_requires = \
['biopython>=1.76,<2.0',
 'click>=7.1.2,<8.0.0',
 'click_loguru>=0.3.3,<0.4.0',
 'click_plugins>=1.1.1,<2.0.0',
 'dask[bag]>=2.15.0,<3.0.0',
 'gffpandas>=1.2.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'sh>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['azulejo = azulejo:cli']}

setup_kwargs = {
    'name': 'azulejo',
    'version': '0.7.0',
    'description': 'tile phylogenetic space with subtrees',
    'long_description': '.. epigraph:: azulejo\n              noun INFORMAL\n              a glazed tile, usually blue, found on the inside of churches and palaces in Spain and Portugal.\n\nazulejo\n=======\n``azulejo`` azulejo tiles phylogenetic space with subtrees\nnormalizes and validates genomic data files prior to further processing\nor inclusion in a data store such as that of the\n`Legume Federation <https://www.legumefederation.org/en/data-store/>`_.\n\nPrerequisites\n-------------\nPython 3.6 or greater is required.\nThis package is tested under Linux and MacOS using Python 3.7.\n\nInstallation for Users\n----------------------\nInstall via pip or (better yet) `pipx <https://pipxproject.github.io/pipx/>`_: ::\n\n     pipx install azulejo\n\n``azulejo`` contains some long commands and many options.  To enable command-line\ncompletion for ``azulejo`` commands, execute the following command if you are using\n``bash`` as your shell: ::\n\n    eval "$(_AZULEJO_COMPLETE=source_bash azulejo)"\n\nFor Developers\n--------------\nIf you plan to develop ``azulejo``, you\'ll need to install\nthe `poetry <https://python-poetry.org>`_ dependency manager.\nIf you haven\'t previously installed ``poetry``, execute the command: ::\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nNext, get the master branch from GitHub ::\n\n\tgit clone https://github.com/legumeinfo/azulejo.git\n\nChange to the ``azulejo/`` directory and install with poetry: ::\n\n\tpoetry install -v\n\nRun ``azulejo`` with ``poetry``: ::\n\n    poetry run azulejo\n\nUsage\n-----\nInstallation puts a single script called ``azulejo`` in your path.  The usage format is::\n\n    azulejo [GLOBALOPTIONS] COMMAND [COMMANDOPTIONS][ARGS]\n\nGlobal Options\n--------------\nThe following options are global in scope and, if used must be placed before\n``COMMAND``:\n\n============================= ===========================================\n   -v, --verbose              Log debugging info to stderr.\n   -q, --quiet                Suppress logging to stderr.\n   --no-logfile               Suppress logging to file.\n   -e, --warnings_as_errors   Treat warnings as fatal (for testing).\n============================= ===========================================\n\nCommands\n--------\nA listing of commands is available via ``azulejo --help``.\nThe currently implemented commands are:\n\n========================= ==================================================\n  add-singletons          Add singleton clusters to cluster file.\n  adjacency-to-graph      Turn adjacency data into GML graph file.\n  analyze-clusters        Statistics of clustering as function of identity.\n  annotate-homology       Marshal homology and sequence information.\n  cluster-in-steps        Cluster in steps from low to 100% identity.\n  clusters-to-histograms  Compute histograms from cluster file.\n  combine-clusters        Combine synteny and homology clusters,\n  compare-clusters        compare one cluster file with another\n  dagchainer-synteny      Read DAGchainer synteny into homology frames.\n  length-std-dist         Plot length distribution of singletons in clusters\n  outlier-length-dist     Plot length distribution of outliers in clusters.\n  prepare-protein-files   Sanitize and combine protein FASTA files.\n  proxy-genes             Calculate a set of proxy genes from synteny files.\n  synteny-anchors         Calculate synteny anchors.\n  usearch-cluster         Cluster at a global sequence identity threshold.\n========================= ==================================================\n\nEach command has its ``COMMANDOPTIONS``, which may be listed with: ::\n\n    azulejo COMMAND --help\n\nProject Status\n--------------\n+-------------------+------------+------------+\n| Latest Release    | |pypi|     | |azulejo|  |\n+-------------------+------------+            +\n| GitHub            | |repo|     |            |\n+-------------------+------------+            +\n| License           | |license|  |            |\n+-------------------+------------+            +\n| Travis Build      | |travis|   |            |\n+-------------------+------------+            +\n| Coverage          | |coverage| |            |\n+-------------------+------------+            +\n| Code Grade        | |codacy|   |            |\n+-------------------+------------+            +\n| Dependencies      | |depend|   |            |\n+-------------------+------------+            +\n| Issues            | |issues|   |            |\n+-------------------+------------+------------+\n\n\n.. |azulejo| image:: docs/azulejo.jpg\n     :target: https://en.wikipedia.org/wiki/Azulejo\n     :alt: azulejo Definition\n\n.. |pypi| image:: https://img.shields.io/pypi/v/azulejo.svg\n    :target: https://pypi.python.org/pypi/azulejo\n    :alt: Python package\n\n.. |repo| image:: https://img.shields.io/github/commits-since/legumeinfo/azulejo/0.3.svg\n    :target: https://github.com/legumeinfo/azulejo\n    :alt: GitHub repository\n\n.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n    :target: https://github.com/legumeinfo/azulejo/blob/master/LICENSE\n    :alt: License terms\n\n.. |rtd| image:: https://readthedocs.org/projects/azulejo/badge/?version=latest\n    :target: http://azulejo.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Server\n\n.. |travis| image:: https://img.shields.io/travis/legumeinfo/azulejo.svg\n    :target:  https://travis-ci.org/legumeinfo/azulejo\n    :alt: Travis CI\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/99549f0ed4e6409e9f5e80a2c4bd806b\n    :target: https://www.codacy.com/app/joelb123/azulejo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=legumeinfo/azulejo&amp;utm_campaign=Badge_Grade\n    :alt: Codacy.io grade\n\n.. |coverage| image:: https://codecov.io/gh/legumeinfo/azulejo/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/legumeinfo/azulejo\n    :alt: Codecov.io test coverage\n\n.. |issues| image:: https://img.shields.io/github/issues/LegumeFederation/lorax.svg\n    :target:  https://github.com/legumeinfo/azulejo/issues\n    :alt: Issues reported\n\n.. |requires| image:: https://requires.io/github/legumeinfo/azulejo/requirements.svg?branch=master\n     :target: https://requires.io/github/legumeinfo/azulejo/requirements/?branch=master\n     :alt: Requirements Status\n\n.. |depend| image:: https://api.dependabot.com/badges/status?host=github&repo=legumeinfo/azulejo\n     :target: https://app.dependabot.com/accounts/legumeinfo/repos/203668510\n     :alt: dependabot dependencies\n',
    'author': 'Joel Berendzen',
    'author_email': 'joelb@ncgr.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/legumeinfo/azulejo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
