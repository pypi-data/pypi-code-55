# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsparams']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.10,<2.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['awsparams = awsparams.cli:main']}

setup_kwargs = {
    'name': 'awsparams',
    'version': '1.2.0',
    'description': 'A simple CLI and Library for adding/removing/renaming/copying AWS Param Store Parameters',
    'long_description': '# Note\nVersion 1 of this library is drastically different than previous versions.\nThe CLI Application hasn\'t changed but the library it uses has.\nPlease pay extra attention to the examples below or look at the underlying class for more information.\n\n# Why this script?\n\nThe current (Jul 2017) AWS Console for the Systems Manager Parameter\nStore is good for adding and editing the values of parameters, but\nmisses key productivity functions like copying (especially en mass),\nrenaming, etc. The current `aws ssm` CLI is very similar in\nfunctionality to the AWS Console.\n\nThis script is to automate a lot of the manual work currently needed\nwith the existing AWS-provided UIs.\n\n# Docs\nFull documentation can be found here: https://awsparams.readthedocs.io/en/latest/\n\n# Installation\n\n  - AWSParams requires Python 3.6+\n  - Depending on your Python3.6 install either `pip install awsparams` or `pip3 install awsparams`\n\n# Usage\n## Library:\n\n```python\nfrom awsparams import AWSParams\n \n# Using default Profile\naws_params = AWSParams()\n\n# Using a Custome Profile\naws_params = AWSParams(\'MyProfile\')\n\n#get a single parameter\nparam = get_parameter(\'test1\')\n# ParamResult(Name=\'test1\', Value=\'test123\', Type=\'SecureString\')\n\n#ParamResult is a named tuple with properties Name, Value, Type\nparam.Name # \'test1\'\nparam.Value # \'test123\'\nparam.Type # \'SecureString\'\n\n# get multiple parameters with a prefix\nparams = get_all_parameters(prefix="testing.testing.")\n# [ParamResult(Name=\'testing\', Value=\'1234\', Type=\'String\'),\n#  ParamResult(Name=\'testing2\', Value=\'1234\', Type=\'String\')]\n\n# get multiple parameters by path\nparams = get_all_parameters(prefix="/testing/testing/", by_path=True)\n# [ParamResult(Name=\'testing\', Value=\'1234\', Type=\'String\'),\n#  ParamResult(Name=\'testing2\', Value=\'1234\', Type=\'String\')]\n\n# get multiple parameters by path\nparams = get_all_parameters(prefix="/testing/testing/", by_path=True, trim_name=False)\n# [ParamResult(Name=\'/testing/testing/testing\', Value=\'1234\', Type=\'String\'),\n#  ParamResult(Name=\'/testing/testing/testing2\', Value=\'1234\', Type=\'String\')]\n\n# get just a parameter value\nvalue = get_parameter_value(\'test1\')\n# test123\n```\nFor more detailed examples of usage as a library see the cli implementation [here](https://github.com/byu-oit/awsparams/blob/master/awsparams/cli.py).\n\n## CLI application:\nUsage can be referenced by running `awsparams --help` or `awsparams\nsubcommand --help` commands:\n\n    Usage: awsparams [OPTIONS] COMMAND [ARGS]...\n    \n    Options:\n    --version  Show the version and exit.\n    --help     Show this message and exit.\n    \n    Commands:\n    cp   Copy a parameter, optionally across accounts\n    ls   List Paramters, optional matching a specific...\n    mv   Move or rename a parameter\n    new  Create a new parameter\n    rm   Remove/Delete a parameter\n    set  Edit an existing parameter\n\n# Command Examples\n\n## ls usage\n\nls names only: `awsparams ls`\n\nls with values no decryption: `awsparams ls --values` or `awsparams ls -v`\n\nls with values and decryption: `awsparams ls --with-decryption`\n\nls by prefix: `awsparams ls appname.prd`\n\n## new usage\n\nnew interactively: `awsparams new`\n\nnew semi-interactively: `awsparams new --name appname.prd.username`\n\nnew non-interactive: `awsparams new --name appname.prd.usrname --value parameter_value\n--description parameter_descripton`\n\n## cp usage\n\ncopy a parameter: `awsparams cp appname.prd.username newappname.prd.username`\n\ncopy set of parameters with prefix appname.dev. to appname.prd.: `awsparams cp appname.dev. appname.prd. --prefix`\n\ncopy set of parameters starting with prefix repometa-generator.prd\noverwrite existing parameters accross different accounts: `awsparams cp repometa-generator.prd --src_profile=dev --dst_profile=trn\n--prefix=True`\n\ncopy single parameters accross different accounts: `awsparams cp appname.dev.username appname.trb.us`',
    'author': 'Nate Peterson',
    'author_email': 'ndpete@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/byu-oit/awsparams',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
