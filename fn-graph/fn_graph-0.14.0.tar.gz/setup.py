# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_graph', 'fn_graph.examples', 'fn_graph.tests']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.13.2,<0.14.0', 'littleutils>=0.2.1,<0.3.0', 'networkx>=2.4,<3.0']

extras_require = \
{'examples': ['seaborn>=0.10.0,<0.11.0',
              'statsmodels>=0.11.1,<0.12.0',
              'matplotlib>=3.0,<4.0',
              'sklearn>=0.0,<0.1',
              'plotly>=4.0,<5.0',
              'pandas>=0.25.3,<0.26.0',
              'yfinance>=0.1,<0.2']}

setup_kwargs = {
    'name': 'fn-graph',
    'version': '0.14.0',
    'description': 'Manage, maintain and reuse complex function graphs without the hassle.',
    'long_description': "# Fn Graph\n\nLightweight function pipelines for python\n\nFor more information and live examples look at [fn-graph.businessoptics.biz](https://fn-graph.businessoptics.biz/)\n\n## Overview\n\n`fn_graph` is trying to solve a number of problems in the python data-science/modelling domain, as well as making it easier to put such models into production.\n\nIt aims to:\n\n1. Make moving between the analyst space to production, and back, simpler and less error prone.\n2. Make it easy to view the intermediate results of computations to easily diagnose errors.\n3. Solve common analyst issues like creating reusable, composable pipelines and caching results.\n4. Visualizing models in an intuitive way.\n\nThere is an associated visual studio you should check out at https://github.com/BusinessOptics/fn_graph_studio/.\n\n## Documentation\n\nPlease find detailed documentation at https://fn-graph.readthedocs.io/\n\n## Installation\n\n```sh\npip install fn_graph\n```\n\nYou will need to have graphviz and the development packages installed. On ubuntu you can install these with:\n\n```sh\nsudo apt-get install graphviz graphviz-dev\n```\n\nOtherwise see the [pygraphviz documentation](http://pygraphviz.github.io/documentation/pygraphviz-1.5/install.html).\n\nTo run all the examples install\n\n```sh\npip install fn_graph[examples]\n```\n\n## Features\n\n* **Manage complex logic**\\\nManage your data processing, machine learning, domain or financial logic all in one simple unified framework. Make models that are easy to understand at a meaningful level of abstraction.\n* **Hassle free moves to production**\\\nTake the models your data-scientist and analysts build and move them into your production environment, whether thats a task runner, web-application, or an API. No recoding, no wrapping notebook code in massive and opaque functions. When analysts need to make changes they can easily investigate all the models steps.\n* **Lightweight**\\\nFn Graph is extremely minimal. Develop your model as plain python functions and it will connect everything together. There is no complex object model to learn or heavy weight framework code to manage.\n* **Visual model explorer**\\\nEasily navigate and investigate your models with the visual fn_graph_studio. Share knowledge amongst your team and with all stakeholders. Quickly isolate interesting results or problematic errors. Visually display your results with any popular plotting libraries.\n* **Work with or without notebooks**\\\nUse fn_graph as a complement to your notebooks, or use it with your standard development tools, or both.\n\n* **Works with whatever libraries you use**\\\nfn_graph makes no assumptions about what libraries you use. Use your favorite machine learning libraries like, scikit-learn, PyTorch. Prepare your data with data with Pandas or Numpy. Crunch big data with PySpark or Beam. Plot results with matplotlib, seaborn or Plotly. Use statistical routines from Scipy or your favourite financial libraries. Or just use plain old Python, it's up to you.\n* **Useful modelling support tools**\\\nIntegrated and intelligent caching improves modelling development iteration time, a simple profiler works at a level that's meaningful to your model.\n** *Easily compose and reuse models**\\\nThe composable pipelines allow for easy model reuse, as well as building up models from simpler submodels. Easily collaborate in teams to build models to any level of complexity, while keeping the individual components easy to understand and well encapsulated.\n* **It's just Python functions**\\\nIt's just plain Python! Use all your existing knowledge, everything will work as expected. Integrate with any existing python codebases. Use it with any other framework, there are no restrictions.\n\n## Similar projects\n\nAn incomplete comparison to some other libraries, highlighting the differences:\n\n**Dask**\n\nDask is a light-weight parallel computing library. Importantly it has a Pandas compliant interface. You may want to use Dask inside FnGraph.\n\n**Airflow**\n\nAirflow is a task manager. It is used to run a series of generally large tasks in an order that meets their dependencies, potentially over multiple machines. It has a whole scheduling and management apparatus around it. Fn Graph is not trying to do this. Fn Graph is about making complex logic more manageable, and easier to move between development and production. You may well want to use Fn Graph inside your airflow tasks.\n\n**Luigi**\n\n> Luigi is a Python module that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization etc. It also comes with Hadoop support built in.\n\nLuigi is about big batch jobs, and managing the distribution and scheduling of them. In the same way that airflow works ate a higher level to FnGraph, so does luigi.\n\n**d6tflow**\n\nd6tflow is similar to FnGraph. It is based on Luigi. The primary difference is the way the function graphs are composed. d6tflow graphs can be very difficult to reuse (but do have some greater flexibility). It also allows for parallel execution. FnGraph is trying to make very complex pipelines or very complex models easier to mange, build, and productionise.\n",
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BusinessOptics/fn_graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
