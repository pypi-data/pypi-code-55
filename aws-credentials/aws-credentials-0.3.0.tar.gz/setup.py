# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_credentials']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.37,<2.0.0']

entry_points = \
{'console_scripts': ['aws-credentials = aws_credentials.cli:main']}

setup_kwargs = {
    'name': 'aws-credentials',
    'version': '0.3.0',
    'description': 'AWS credential manager',
    'long_description': '# AWS Credentials\n\nThis tool lets you easily manage AWS IAM Credentials for a user.\n\n## Usage\n```\n⇒  aws-credentials --help\nusage: aws-credentials [-h]\n                       {activate,create,deactivate,delete,list,rotate} ...\n\nUtility for managing AWS access keys.\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nCommands:\n  {activate,create,deactivate,delete,list,rotate}\n    activate            Activate a specific access key.\n    create              Create a new access key.\n    deactivate          Deactivate a specific access key.\n    delete              Delete a specific access key.\n    list                List access keys.\n    rotate              Rotate AWS credentials.\n```\n\n**activate**\n```\n⇒  aws-credentials activate --help\nusage: aws-credentials activate [-h] [-v]\n                                [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                                [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                                [--aws-session-token AWS_SESSION_TOKEN]\n                                access_key_id\n\nActivate a specific access key.\n\npositional arguments:\n  access_key_id         id of the key to activate.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n\n**create**\n```\n⇒  aws-credentials create --help\nusage: aws-credentials create [-h] [-v]\n                              [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                              [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                              [--aws-session-token AWS_SESSION_TOKEN]\n\nCreate a new access key.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n\n**deactivate**\n```\n⇒  aws-credentials deactivate --help\nusage: aws-credentials deactivate [-h] [-v]\n                                  [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                                  [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                                  [--aws-session-token AWS_SESSION_TOKEN]\n                                  access_key_id\n\nDeactivate a specific access key.\n\npositional arguments:\n  access_key_id         id of the key to deactivate.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n\n**delete**\n```\n⇒  aws-credentials delete --help\nusage: aws-credentials delete [-h] [-v]\n                              [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                              [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                              [--aws-session-token AWS_SESSION_TOKEN]\n                              access_key_id\n\nDelete a specific access key.\n\npositional arguments:\n  access_key_id         id of the key to delete.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n\n**list**\n```\n⇒  aws-credentials list --help\nusage: aws-credentials list [-h] [-v] [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                            [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                            [--aws-session-token AWS_SESSION_TOKEN]\n\nList access keys.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n\n**rotate**\n```\n⇒  aws-credentials rotate --help\nusage: aws-credentials rotate [-h] [-v]\n                              [--aws-access-key-id AWS_ACCESS_KEY_ID]\n                              [--aws-secret-access-key AWS_SECRET_ACCESS_KEY]\n                              [--aws-session-token AWS_SESSION_TOKEN]\n\nRotate AWS credentials. This will delete inactive keys before creating the new\nkey. It will then deactivate the old key.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase the verbosity of messages. "-v" for normal\n                        output, and "-vv" for more verbose output.\n  --aws-access-key-id AWS_ACCESS_KEY_ID\n                        AWS_ACCESS_KEY_ID to use.\n  --aws-secret-access-key AWS_SECRET_ACCESS_KEY\n                        AWS_SECRET_ACCESS_KEY to use.\n  --aws-session-token AWS_SESSION_TOKEN\n                        AWS_SESSION_TOKEN to use.\n```\n',
    'author': 'Paul Robertson',
    'author_email': 't.paulrobertson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/perobertson/aws-credentials',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
