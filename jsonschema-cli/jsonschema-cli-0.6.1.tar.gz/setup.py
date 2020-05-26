# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_cli', 'jsonschema_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['jsonschema-cli = jsonschema_cli.cli:run']}

setup_kwargs = {
    'name': 'jsonschema-cli',
    'version': '0.6.1',
    'description': 'A thin wrapper over [Python Jsonschema](https://github.com/Julian/jsonschema) to allow validating shcemas easily using simple CLI commands.',
    'long_description': '# JsonSchema CLI\n\nA thin wrapper over [Python Jsonschema](https://github.com/Julian/jsonschema) to allow validating shcemas easily using simple CLI commands.\n\n## Installing\n\n`pip install jsonschema-cli`\n\n## Security\n\nThe `$ref` resolving will automatically resolve to any path using basic `$ref` notation:\n\n```json\n{"$ref": "my-custom.json#...."}\n```\n\nThat means that when using this tool, an attacker may do the following:\n\n```json\n{"$ref": "../../../../all-my-secrets.json"}\n```\n\nTo make sure this doesn\'t happen:\n\n1. When using this tool in a backend server, make sure the file access is scoped.\n2. Don\'t run JSONSCHEMAS without sanitizing paths.\n3. Treat all un-knwon user input as evil.\n\nThis has no actual current  affect other than loading the contets of secrets into memory of the process.\nBut may lead to misfortune if not addressed.\n\n## Usgae\n\nUsing `jsonschema-cli --help`\n\n```bash\nusage: jsonschema-cli [-h] {validate} ...\n\nA wrapper around https://github.com/Julian/jsonschema to validate JSON using the CLI\n\npositional arguments:\n  {validate}  Validate thet json data with a schema\n    validate  Validate\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\n### Validate\n\nUsing `jsonschema-cli validate --help`\n\n```bash\nusage: jsonschema-cli validate [-h] schema_file_or_string data_file_or_string\n\npositional arguments:\n  schema_file_or_string\n                        The schema you want to use to validate the data\n  data_file_or_string   The data you want validated by the schema\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\n### Examples\n\n```bash\n# Returns no errors on stdout, no output needed on success (just exit code 0 is enough)\njsonschema-cli validate \'{"properties": {"number": {"type": "integer"}}, "required": ["number"]}\' \'{"number": 123}\'\n# Has an error, "number" is now "123" instead of 123, an integer is expected.\njsonschema-cli validate \'{"properties": {"number": {"type": "integer"}}, "required": ["number"]}\' \'{"number": "123"}\'\n> \'123\' is not of type \'integer\'\n>\n> Failed validating \'type\' in schema[\'properties\'][\'number\']:\n>     {\'type\': \'integer\'}\n>\n> On instance[\'number\']:\n>     \'123\'\n```\n\n## Load YAML\n\nThe CLI command can read YAML and validate both schema and data written in YAML\n\n```bash\n# Returns no errors on stdout, no output needed on success (just exit code 0 is enough)\nSCHEMA="\nproperties:\n  number:\n    type: integer\n"\nDATA="\nnumber: 123\n"\njsonschema-cli validate "$SCHEMA" "$DATA"\n# Has an error, "number" is now "123" instead of 123, an integer is expected.\nSCHEMA="\nproperties:\n  number:\n    type: integer\n"\nDATA="\nnumber: \\"123\\"\n"\njsonschema-cli validate "$SCHEMA" "$DATA"\n> \'123\' is not of type \'integer\'\n>\n> Failed validating \'type\' in schema[\'properties\'][\'number\']:\n>     {\'type\': \'integer\'}\n>\n> On instance[\'number\']:\n>     \'123\'\n```\n',
    'author': 'Eyal Mor',
    'author_email': 'eyalmor94@gmail.com',
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
