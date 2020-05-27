# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['env_resolver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'env-resolver',
    'version': '0.1.6',
    'description': 'A utility for resolving ssm parameters and secretsmanager secrets',
    'long_description': "# ENV Resolver (Python)\n\n![](https://github.com/wulfmann/env-resolver/workflows/CI/badge.svg)\n\nThis is a small utility to resolve [SSM Parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) and [Secretsmanager Secrets](https://aws.amazon.com/secrets-manager/) and conditionally set them in the environment.\n\nThis is helpful for services like [AWS Batch](https://aws.amazon.com/batch/) or [AWS Lambda](https://aws.amazon.com/lambda/) where there is not a way natively to pass secret values.\n\n## Install\n\n```bash\npip install env-resolver\n```\n\nThis package assumes that you already depend on [boto3](https://github.com/boto/boto3) and have it installed as a dependency of your project. If you are using this package in [AWS Lambda](https://aws.amazon.com/lambda/), `boto3` will already be available.\n\n## Quick Start\n\n### Parameter Store\n\n```python\nfrom parameter_resolver import resolve\n\n# assuming you've created two parameters:\n# ssm/parameter/env-one = val-one\n# ssm/parameter/env-two = val-two\n\nparameters = {\n    'ENV_ONE': 'ssm/parameter/env-one',\n    'ENV_TWO': 'ssm/parameter/env-two'\n}\n\nprint(resolve('ssm', parameters))\n\n# Outputs:\n# {\n#     'ENV_ONE': 'val-one',\n#     'ENV_TWO': 'val-two'\n# }\n```\n\n### Secrets Manager\n\n```python\nfrom parameter_resolver import resolve\n\n# assuming you've created the following secret:\n# secret/secret-one =\n# {\n#     'ENV_ONE': 'val-one',\n#     'ENV_TWO': 'val-two'\n# }\n\nsecret = {\n    'secret_id': 'secret/secret-one'\n}\n\nprint(resolve('secretsmanager', secret))\n\n# Outputs:\n# {\n#     'ENV_ONE': 'val-one',\n#     'ENV_TWO': 'val-two'\n# }\n```\n\n## Usage\n\n```text\nresolve(parameter_type, parameter_value, set_environment_variables=True)\n```\n\nThese are the possible values for `parameter_type`:\n\n* ssm\n* secretsmanager\n\n## Options\n\nThe `set_environment_variables` options allows you to choose whether or not to set the new `key-value` pairs in the environment.\n\n### SSM\n\nFor a parameter store parameter, `resolve` expects the `parameter_value` to be a dictionary of `KEY`: `PARAMETER_NAME`.\n\n### Secretsmanager\n\nFor a secretsmanager secret, `resolve` expects the `parameter_value` to be a dictionary with the following possible values:\n\n```python\nsecret = {\n    'secret_id': 'string',\n    'version_id': 'string', # optional\n    'json_value': 'boolean' # option, default=True\n}\n```\n\n## Contributing\n\nPR's are welcome!\n\nThis project uses [Poetry](https://python-poetry.org/) for dependency / environment management.\n\n### Install Dependencies\n\n```bash\npoetry install\n```\n\n### Tests\n\n```bash\npoetry run pytest\n```\n",
    'author': 'Joe Snell',
    'author_email': 'joepsnell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wulfmann/env-resolver/python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
