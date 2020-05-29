# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poethepoet', 'poethepoet.cli']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['poe = poethepoet.cli:main']}

setup_kwargs = {
    'name': 'poethepoet',
    'version': '0.0.2',
    'description': 'A task runner that works well with poetry.',
    'long_description': "************\nPoe the Poet\n************\n\nA task runner that works well with poetry.\n\nFeatures\n========\n\n- Straight foward declaration of project tasks in your pyproject.toml (kind of like npm scripts)\n- Task are run in poetry's virtualenv by default\n- Short and sweet commands ``poe [options] task [task_args]``\n\nInstallation\n============\n\n.. code-block:: bash\n\n  pip install poethepoet\n\nUsage\n=====\n\nDefine tasks in your pyproject.toml\n-----------------------------------\n\n`See a real example <https://github.com/nat-n/poethepoet/blob/master/pyproject.toml>`_\n\n.. code-block:: toml\n\n  [tool.poe.tasks]\n  test = pytest --cov=poethepoet\n\nRun tasks with the poe cli\n--------------------------\n\n.. code-block:: bash\n\n  poe test\n\nAdditional argument are passed to the task so\n\n.. code-block:: bash\n\n  poe test -v tests/favorite_test.py\n\nresults in\n\n.. code-block:: bash\n\n  pytest --cov=poethepoet -v tests/favorite_test.py\n\nYou can also run it like so if you fancy\n\n.. code-block:: bash\n\n  python -m poethepoet\n\nContributing\n============\n\nPlease do.\n\nTODO\n====\n\n* make the cli more friendly with colors and supportive helpful messages\n* support running tasks outside of poetry's virtualenv (or in another?)\n* the abiltiy to declare specific arguments for a task\n* test better\n* task aliases\n* more nuanced awareness of virtualenv\n\nLicence\n=======\n\nMIT. Go nuts.\n",
    'author': 'Nat Noordanus',
    'author_email': 'n@natn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nat-n/poethepoet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
