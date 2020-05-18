# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['periskop_client']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'periskop-client',
    'version': '0.1.0',
    'description': 'Periskop Python client',
    'long_description': '# periskop-python\n\n[![Build Status](https://api.cirrus-ci.com/github/soundcloud/periskop-python.svg)](https://cirrus-ci.com/github/soundcloud/periskop-python)\n\n[Periskop](https://github.com/soundcloud/periskop) requires collecting and aggregating exceptions on the client side,\nas well as exposing them via an HTTP endpoint using a well defined format.\n\nThis library provides low level collection and rendering capabilities\n\n## Install\n\n```\npip install periskop-client\n```\n\n## Usage example\n\n```python\nimport json\nfrom http.server import HTTPServer\n\nfrom periskop_client.collector import ExceptionCollector\nfrom periskop_client.exporter import ExceptionExporter\nfrom periskop_client.handler import exception_http_handler\nfrom periskop_client.models import HTTPContext\n\n\ndef faulty_json():\n    return json.loads(\'{"id":\')\n\n\nif __name__ == "__main__":\n    collector = ExceptionCollector()\n    try:\n        faulty_json()\n    except Exception as exception:\n        # Report without context\n        collector.report(exception)\n        # Report with HTTP context\n        collector.report_with_context(\n            exception,\n            HTTPContext("GET", "http://example.com", {"Cache-Control": "no-cache"}),\n        )\n\n    # Expose collected exceptions in localhost:8081/-/exceptions\n    server_address = ("", 8081)\n    handler = exception_http_handler(\n        path="/-/exceptions", exporter=ExceptionExporter(collector)\n    )\n    http_server = HTTPServer(server_address, handler)\n    http_server.serve_forever()\n```\n\n## Run tests\n\nFor running tests [pytest](https://docs.pytest.org) is needed. A recommended way to run all check is installing [tox](https://tox.readthedocs.io/en/latest/install.html) and then just type `tox`. This will run `pytest` tests, [black](https://black.readthedocs.io) formatter and [flake8](https://flake8.pycqa.org) and [mypy](http://mypy-lang.org/) static code analyzers.\n\nAlternatively you can run `pip install -r requirements-tests.txt` and then run `pytest`.\n',
    'author': 'Marc Tuduri',
    'author_email': 'marc.tuduri@soundcloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
