# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcr_stub_server', 'vcr_stub_server.cassettes']

package_data = \
{'': ['*']}

install_requires = \
['vcrpy>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['vcr-stub-server = vcr_stub_server.__main__:main']}

setup_kwargs = {
    'name': 'vcr-stub-server',
    'version': '0.1.4',
    'description': 'Standalone stub server for replaying VCR cassettes',
    'long_description': "# vcr-stub-server\n\n[![PyPI version](https://badge.fury.io/py/vcr-stub-server.svg)](https://pypi.org/project/vcr-stub-server/)\n\nThis is a small tool for setting up a lightweight stub server that replays previously recorded VCR cassettes.\n\nUsually VCR is used internally while running the test suite. In that case, the library is responsible for intercepting HTTP requests. \n\nBut in some cases, it can be useful to be able to spin up a live HTTP server which given a preexisting VCR cassette, would respond to each request with its matching recorded response.\n\nOne such case might come when implementing usage of [Pact](http://pact.io), where `vcr-stub-server` can be used to prevent the provider service from making requests to external services during pact verification. This project was inspired by Pact's own [Stub Service](https://github.com/pact-foundation/pact-mock_service#stub-service-usage).\n\n#### Caveats\n\n- Unfortunately, there is no one standard for cassette YAML files, each VCR implementation is different. For example, cassette YAML files created by VCR.py won't be compatible with YAML files created by the Ruby implementation of VCR, etc.\n\n  Therfore **this tool currently only supports [VCR.py](https://github.com/kevin1024/vcrpy)**, using the library's own implementation of parsing the YAML files.\n  \n- The recorded requests in your YAML cassette file must all be made to the same host.\n\n## Installation\n\n```\n$ pip install vcr-stub-server\n```\n\n## Usage\n\nOnce the package is installed, use the `vcr-stub-server` command to spin up your stub server.\n\n```\n$ vcr-stub-server path/to/vcr_cassette.yml\n```\n\n## Contributing\n\nBug reports and pull requests are welcome on GitHub at https://github.com/thatguysimon/vcr-stub-server. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](https://contributor-covenant.org) code of conduct.\n\n## License\n\nThe gem is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n",
    'author': 'Simon Nizov',
    'author_email': 'simon.nizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thatguysimon/vcr-stub-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
