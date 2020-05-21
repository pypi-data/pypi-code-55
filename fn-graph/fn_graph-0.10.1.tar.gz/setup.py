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
              'pandas>=0.25.3,<0.26.0']}

setup_kwargs = {
    'name': 'fn-graph',
    'version': '0.10.1',
    'description': 'Manage, maintain and reuse complex function graphs without the hassle.',
    'long_description': '# Fn Graph\n\nLight weight function pipelines for python.\n\n## Overview\n\n`fn_graph` is trying to solve a number of problems in the python data-science/modelling domain, as well as making it easier to put such models into production.\n\nIt aims to:\n\n1. Make moving between the analyst space to production. amd back, simpler and less error prone.\n2. Make it easy to view the intermediate results of computations to easily diagnose errors.\n3. Solve common analyst issues like creating reusable, composable pipelines and caching results.\n4. Visualizing models in an intuitive way.\n\nThere is an associated visual studio you should check out at https://github.com/BusinessOptics/fn_graph_studio/.\n\n## Documentation\n\nPlease find detailed documentation at https://fn-graph.readthedocs.io/\n\n## Installation\n\n```\npip install fn_graph\n```\n\nYou will need to have graphviz and the development packages installed. On ubuntu you can install these with:\n\n```\nsudo apt-get install graphviz graphviz-dev\n```\n\nOtherwise see the [pygraphviz documentation](http://pygraphviz.github.io/documentation/pygraphviz-1.5/install.html).\n\n## Outline of the problem\n\nIn complex domains, like financial modelling or data-science, modellers and programmers often have complex logic that needs to be re-used in multiple environments. For example a financial analyst may write a model in a notebook, which then must be placed in a production environment (normally through rewriting the notebook which was not written in a modular or easy to use manner), after which changes need to made, which must be done in the notebook environment, which then need to be moved back into production. This is the stuff of [nightmare fuel](https://www.urbandictionary.com/define.php?term=nightmare%20fuel) for everyone involved.\n\nTo make this process easier the best option is to break functionality into small reusable functions, that can be referenced in both the notebook environment and the production environment. Now you unfortunately you have this bag of small functions whose relationships you have to manage. There are few ways to do this. Assume we have the functions below:\n\n```python\ndef get_a():\n    return 5\n\ndef get_b(a):\n    return a * 5\n\ndef get_c(a, b):\n    return a * b\n```\n\n**Option 1 - Directly compose at call site:**\n\n```python\na = get_a()\nb = get_b(a)\nc = get_c(a, b)\n```\n\n_Pros:_ The modeller can easily see intermediate results\\\n_Cons:_ Now this potentially complex network of function calls has to be copied and pasted between notebooks and production\n\n**Option 2 - Wrap it up in a function that pass around**\n\n```python\ndef composed_c():\n    a = get_a()\n    b = get_b(a)\n    return  get_c(a, b)\n```\n\n_Pros:_ This is easy to reference from both the notebook and production\\\n_Cons:_ The modeller cannot see the intermediate results, so it can be difficult to debug (this is a big problem if you are working with big multi-dimensional objects that you may want to visualize, a debugger does not cut it)\n\n**Option 3 - Directly call functions from each other**\n\n```python\ndef get_a():\n    return 5\n\ndef get_b(a):\n    return get_a() * 5\n\ndef get_c():\n    return get_a() * get_b()\n```\n\n_Pros:_ This is easy to reference from both the notebook and production\\\n_Cons:_ The modeller cannot see the intermediate results and functions cannot be reused. Functions are called multiple times.\n\nNone of these are great. Fn Graph would solve it like this.\n\n```python\nfrom fn_graph import Composer\n\ndef a():\n    return 5\n\ndef b(a):\n    return a * 5\n\ndef c(a, b):\n    return a * b\n\ncomposer = Composer().update(a, b, c)\n\n# Call any result\ncomposer.c() # 125\ncomposer.a() # 5\n\ncomposer.graphviz()\n```\n\n![Graph of composer](intro.gv.png)\n\nThe composer can then be easily passed around in both the production and notebook environment. It can do much more than this.\n\n## Features\n\n- Manage complex function graphs, including using namespaces.\n- Update composers to gradually build more and more complex logic.\n- Enable incredible function reuse.\n- Visualize logic to make knowledge sharing easier.\n- Perform graph operations on composers to dynamically rewire your logic.\n- Manage calculation life cycle, with hooks, and have access to all intermediary calculations.\n- Cache results, either within a single session, or between sessions in development mode. Using the development cache intelligently invalidate the cache when code changes .\n\n## Similar projects\n\n**Dask**\n\nDask is a light-weight parallel computing library. Importantly it has a Pandas compliant interface. You may want to use Dask inside FnGraph.\n\n**Airflow**\n\nAirflow is a task manager. It is used to run a series of generally large tasks in an order that meets their dependencies, potentially over multiple machines. It has a whole scheduling and management apparatus around it. Fn Graph is not trying to do this. Fn Graph is about making complex logic more manageable, and easier to move between development and production. You may well want to use Fn Graph inside your airflow tasks.\n\n**Luigi**\n\n> Luigi is a Python module that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization etc. It also comes with Hadoop support built in.\n\nLuigi is about big batch jobs, and managing the distribution and scheduling of them. In the same way that airflow works ate a higher level to FnGraph, so does luigi.\n\n**d6tflow**\n\nd6tflow is very similar to FnGraph. It is based on Luigi. The primary difference is the way the function graphs are composed. d6tflow graphs can be very difficult to reuse (but do have some greater flexibility). It also allows for parallel execution. FnGraph is trying to make very complex pipelines or very complex models easier to mange, build, and productionise.\n',
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
