# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webex_assistant_sdk']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.8,<3.1', 'mindmeld>=4.2.3,<5.0.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['wxa_sdk = webex_assistant_sdk.__main__:main']}

setup_kwargs = {
    'name': 'webex-assistant-sdk',
    'version': '0.1.1',
    'description': 'An SDK for developing applications for Webex Assistant.',
    'long_description': '# Webex Assistant SDK\n\nAn SDK for developing Webex Assistant Skills based on the [MindMeld](www.mindmeld.com) platform.\n\n## Install the SDK\n\n`pip install webex_assistant_sdk`\n\n## Using the SDK\n\nTo use the SDK we just need to import SkillApplication and pass in the RSA private key as well as the secret for verifying the request\'s header.\n\nHere is an example implementation which is found in the `tests` folder:\n\n```python\nimport os\n\nfrom webex_assistant_sdk import SkillApplication\nfrom webex_assistant_sdk.crypto import load_private_key_from_dir\n\nsecret = \'some secret\'\nkey = load_private_key_from_dir(os.path.realpath(os.path.dirname(__file__)), password=None)\napp = SkillApplication(__name__, secret=secret, private_key=key)\n\n__all__ = [\'app\']\n```\n\nSimilar to MindMeld applications, for development convenience, we have included a Flask server for you to test your application.\n\nTo run the development server you can use the `run` command: `python -m [app] run`.\n\nWe do not recommend using the development server for production purpose. To learn more about productionizing Flask application, please check [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/).\n\n### The introduce decorator\n\nThe SkillApplication adds a `introduce` decorator in addition to MindMeld\'s build in decorator. This is used to mark the dialogue state to use when a user calls a skill without any command, i.e. "talk to <skill-name>"\n\n#### Example\n\n```python\n@app.introduce\ndef introduction(request, responder):\n    pass\n```\n\n### Command Line\n\nInstalling the webex_assistant_sdk package adds a wxa_sdk command line application. Use the `-h` argument for help.\n\n```bash\n$ wxa_sdk -h\nusage: wxa_sdk [-h] {new,generate-keys,invoke} ...\n\npositional arguments:\n  {new,generate-keys,invoke}\n    new                 create a new skill project\n    generate-keys       generate keys for use with a Webex Assistant Skill\n    invoke              invoke a skill simulating a request from Webex\n                        Assistant\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n',
    'author': 'Minh Vo Thanh',
    'author_email': 'minhtue@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
