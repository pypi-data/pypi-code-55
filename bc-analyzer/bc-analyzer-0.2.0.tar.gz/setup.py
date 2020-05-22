# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['behaviorcloud', 'behaviorcloud.analyzer']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'deepdiff>=4.3.2,<5.0.0',
 'flake8>=3.8.1,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests==2.23.0',
 'sentry-sdk>=0.14.4,<0.15.0']

setup_kwargs = {
    'name': 'bc-analyzer',
    'version': '0.2.0',
    'description': 'A package to create a BehaviorCloud compatible data analyzer.',
    'long_description': '# BehaviorCloud Analyzer\n#### Python Helper\n\n[![N|Solid](https://behaviorcloud.com/images/section/logo-4ffacbfa.png)](https://behaviorcloud.com/images/section/logo-4ffacbfa.png)\n\nThis is a thin package to help you quickly create a BehaviorCloud analyzer. It will handle calls to the BehaviorCloud API server so you don\'t have to worry about it. This package supports the following features: \n  - Fully managed analyzer creation - you just make the conversion function!\n  - One off analysis (pass an "--id" command-line parameter)\n  - Daemon analysis (use the "--daemon" flag)\n  - Exception handling and automatic upload to Sentry.io\n\nExample Usage:\n```python\nimport json\n\nfrom behaviorcloud.analyzer.data import convert_stream_to_json\nfrom behaviorcloud.analyzer.coordinator import Coordinator\n\ndef convert(source_request, source_settings, settings, source, targets):\n    target = targets[0]\n    source_data = convert_stream_to_json(source_request)\n    analyzed_data = [{processed: True, original: entry} for entry in source_data]\n    return [{\n        "data": json.dumps(analyzed_data),\n        "extension": "json",\n        "id": target["id"],\n    }]\n\ncoordinator = Coordinator(convert)\ncoordinator.run()\n```\n',
    'author': 'Christian Lent',
    'author_email': 'christian@behaviorcloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/behaviorcloud/bc-analyzer-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
