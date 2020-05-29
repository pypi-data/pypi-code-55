# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teal_lang',
 'teal_lang.cli',
 'teal_lang.controllers',
 'teal_lang.examples',
 'teal_lang.executors',
 'teal_lang.machine',
 'teal_lang.run',
 'teal_lang.teal_compiler',
 'teal_lang.teal_parser']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'docopt',
 'graphviz>=0.13.2,<0.14.0',
 'pydot>=1.4.1,<2.0.0',
 'pynamodb',
 'pyyaml>=5.3.1,<6.0.0',
 'schema>=0.7.2,<0.8.0',
 'sly>=0.4,<0.5']

entry_points = \
{'console_scripts': ['teal = teal_lang.cli.main:main']}

setup_kwargs = {
    'name': 'teal-lang',
    'version': '0.2.1',
    'description': 'The Teal Programming Language',
    'long_description': '# The Teal Programming Language\n\n![Tests](https://github.com/condense9/teal-lang/workflows/Build/badge.svg?branch=master) [![PyPI](https://badge.fury.io/py/teal-lang.svg)](https://pypi.org/project/teal-lang) [![Gitter](https://badges.gitter.im/Teal-Lang/community.svg)](https://gitter.im/Teal-Lang/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n\nTeal is a programming language for serverless cloud applications, designed for\npassing data around between Python functions. Concurrency supported. Execution\ntracing built-in.\n\nKey features:\n- Very little infrastructure, for applications of any complexity. The Teal\n  runtime shares 4 Lambda functions and stores execution state in a DynamoDB\n  table.\n- Minimal wasted server time. When your code is waiting for another thread to\n  finish, the Lambda is completely stopped.\n- Simple mental models. Teal programs can be traced, profiled, and the code can\n  be reviewed just like any other language. Want to see where your Python\n  function is being used? Just grep your codebase.\n- Local testing is first-class. Teal programs can be run locally, so you can\n  test your entire workflow before deployment.\n\nTeal runs locally or on AWS Lambda. Teal threads can be suspended while another\nthread finishes. Execution data is stored in memory or in a DynamoDB table.\n\n![Concurrency](doc/functions.png)\n\nDocumentation coming soon! For now, browse the [the examples](test/examples) or\nthe check out the [Teal Playground](https://www.condense9.com/playground).\n\n\n## FAQ\n\n**Why is this not a library/DSL in Python?**\n\nWhen Teal threads wait on a Future, they stop completely. The Lambda function\nsaves the machine state and then terminates. When the Future resolves, the\nresolving thread restarts any waiting threads by invoking new Lambdas to pick up\nexecution.\n\nTo achieve the same thing in Python, the framework would need to dump the entire\nPython VM state to disk, and then reload it at a later point -- I don\'t know\nPython internals well enough to do this, and it felt like a huge task.\n\n**How is Teal like Go?**\n\nGoroutines are very lightweight, while Teal `async` functions are pretty heavy --\nthey involve creating a new Lambda (or process, when running locally).\n\nTeal\'s concurrency model is similar to Go\'s, but channels are not fully\nimplemented so data can only be sent to/from a thread at call/return points.\n\n**Is this an infrastructure-as-code tool?**\n\nNo, Teal doesn\'t create or manage infrastructure. There are already great tools\nto do that ([Terraform](https://www.terraform.io/),\n[Pulumi](https://www.pulumi.com/), [Serverless\nFramework](https://www.serverless.com/), etc). Teal requires infrastructure to\nrun on AWS, and you can set that up however you prefer.\n\nInstead, Teal reduces the amount of infrastructure you need. Instead of a\ndistinct Lambda function for every piece of application logic, you only need the\ncore Teal interpreter Lambda functions.\n\n\n## Getting started\n\n**Teal is alpha quality - don\'t use it for mission critical things.**\n\n```shell\n$ pip install teal-lang\n```\n\nThis gives you the `teal` executable.\n\nBrowse the [the examples](test/examples) to explore the syntax.\n\nCheck out an [example AWS deployment](examples/hello/serverless.yml) using the\nServerless Framework.\n\n[Create an issue](https://github.com/condense9/teal-lang/issues) if none of this\nmakes sense, or you\'d like help getting started.\n\n\n### Teal May Not Be For You!\n\nTeal *is* for you if:\n- you want to build ETL pipelines.\n- you have a repository of data processing scripts, and want to connect them\n  together in the cloud.\n- you insist on being able to test as much as possible locally.\n- You don\'t have time (or inclination) to deploy and manage a full-blown\n  platform (Spark, Airflow, etc).\n- You\'re wary of Step Functions (and similar) because of vendor lock-in and cost.\n\nCore principles guiding Teal design:\n- Do the heavy-lifting in Python.\n- Keep business logic out of infrastructure (no more hard-to-test logic defined\n  in IaC, please).\n- Workflows must be fully tested locally before deployment.\n\n\n## Why Teal?\n\nTeal is **not** Kubernetes, because it\'s not trying to let you easily scale\nDockerised services.\n\nTeal is **not** containerisation, because.. well because there are no containers\nhere.\n\nTeal is **not** a general-purpose programming language, because that would be\nneedlessly reinventing the wheel.\n\nTeal is a very simple compiled language with only a few constructs:\n\n1. named variables (data, functions)\n2. `async`/`await` concurrency primitives \n3. Python (>=3.8) interop\n4. A few basic types\n\nTwo interpreters have been implemented so far -- local and AWS Lambda, but\nthere\'s no reason Teal couldn\'t run on top of (for example) Kubernetes. [Issue\n#8](https://github.com/condense9/teal-lang/issues/8)\n\n**Concurrency**: Teal gives you "bare-metal concurrency" (i.e. without external\ncoordination) on top of AWS Lambda.\n\nWhen you do `y = async f(x)`, Teal computes `f(x)` on a new Lambda instance. And\nthen when you do `await y`, the current Lambda function terminates, and\nautomatically continues when `y` is finished being computed. There\'s no idle\nserver time.\n\n**Testing**: The local interpreter lets you test your program before deployment,\nand uses Python threading for concurrency.\n\n**Tracing and profiling**: Teal has a built-in tracer tool, so it\'s easy to see\nwhere the time is going.\n\n\n## Current Limitations and Roadmap\n\nTeal is alpha quality, which means that it\'s not thoroughly tested, and lots of\nbreaking changes are planned. This is a non-exhaustive list.\n\n### Libraries\n\nOnly one Teal program file is supported, but a module/package system is\n[planned](https://github.com/condense9/teal-lang/issues/9).\n\n### Error Handling\n\nThere\'s no error handling - if your function fails, you\'ll have to restart the\nwhole process manually. An exception handling system is\n[planned](https://github.com/condense9/teal-lang/issues/1).\n\n### Typing\n\nFunction inputs and outputs aren\'t typed. This is a limitation, and will be\nfixed soon, probably using\n[ProtoBufs](https://developers.google.com/protocol-buffers/) as the interface\ndefinition language.\n\n### Calling Arbitrary Services\n\nCurrently you can only call Teal or Python functions -- arbitrary microservices\ncan\'t be called. Before Teal v1.0 is released, this will be possible. You will\nbe able to call a long-running third party service (e.g. an AWS ML service) as a\nnormal Teal function and `await` on the result.\n\n### Dictionary (associative map) primitives\n\nTeal really should be able to natively manipulate JSON objects. This may happen\nbefore v1.0.\n\n---\n\n\n## Contributing\n\nContributions of any form are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)\n\nMinimum requirements to develop:\n- Docker (to run local DynamoDB instance)\n- Poetry (deps)\n\nUse `scripts/run_dynamodb_local.sh` to start the database and web UI. Export the\nenvironment variables it gives you - these are required by the Teal runtime.\n\n\n## Who?\n\nTeal is maintained by [Condense9 Ltd.](https://www.condense9.com/). Get in touch\nwith [ric@condense9.com](ric@condense9.com) for bespoke data engineering and\nother cloud software services.\n\nTeal started because we couldn\'t find any data engineering tools that were\nproductive and *felt* like software engineering. As an industry, we\'ve spent\ndecades growing a wealth of computer science knowledge, but building data\npipelines in $IaC, or manually crafting workflow DAGs with $AutomationTool,\n*just isn\'t software*.\n\n\n## License\n\nApache License (Version 2.0). See [LICENSE](LICENSE) for details.\n',
    'author': 'Ric da Silva',
    'author_email': 'ric@condense9.com',
    'maintainer': 'Ric da Silva',
    'maintainer_email': 'ric@condense9.com',
    'url': 'https://www.condense9.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
