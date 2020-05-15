# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfony']

package_data = \
{'': ['*'], 'pyfony': ['container/*', 'kernel/*', 'kernel/BaseKernelTest/*']}

install_requires = \
['console-bundle>=0.2.5,<0.3.0',
 'injecta>=0.8.1,<0.9.0',
 'logger-bundle>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'pyfony',
    'version': '0.5.0',
    'description': 'Dependency Injection powered framework',
    'long_description': "# Pyfony framework\n\nPyfony is a **Dependency Injection (DI) powered framework** written in Python greatly inspired by the [Symfony Framework](https://symfony.com/) in PHP & [Spring Framework](https://spring.io/projects/spring-framework) in Java.\n\nThe DI functionality is provided by the [Injecta Dependency Injection Container](https://github.com/pyfony/injecta).\n\nPyfony = **Injecta + bundles (extensions) API**\n\n## Installation\n\n```\n$ pip install pyfony\n```\n\n## Pyfony initialization\n\n(The following steps are covered in the [BaseKernelTest](src/pyfony/kernel/BaseKernelTest.py))\n\nTo start using Pyfony, create a simple `config_dev.yaml` file to define your DI services:\n\n```yaml\nparameters:\n  api:\n    endpoint: 'https://api.mycompany.com'\n\nservices:\n    mycompany.api.ApiClient:\n      arguments:\n        - '@mycompany.api.Authenticator'\n\n    mycompany.api.Authenticator:\n      class: mycompany.authenticator.RestAuthenticator\n      arguments:\n        - '%api.endpoint%'\n        - '%env(API_TOKEN)%'\n```\n\nThen, initialize the container:\n\n```python\nfrom injecta.config.YamlConfigReader import YamlConfigReader\nfrom pyfony.kernel.BaseKernel import BaseKernel\n\nappEnv = 'dev'\n\nkernel = BaseKernel(\n    appEnv,\n    '/config/dir/path', # must be directory, not the config_dev.yaml file path!\n    YamlConfigReader()\n)\n\ncontainer = kernel.initContainer()\n```\n\nUse `container.get()` to finally retrieve your service:\n\n```python\nfrom mycompany.api.ApiClient import ApiClient\n\napiClient = container.get('mycompany.api.ApiClient') # type: ApiClient   \napiClient.get('/foo/bar')\n```\n\n## Advanced examples\n\nFor more examples, see the [Injecta documentation](https://github.com/pyfony/injecta/blob/master/README.md)\n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/pyfony',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
