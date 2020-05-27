# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renpy_distribute_tools']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.4.4,<3.0.0']

setup_kwargs = {
    'name': 'renpy-distribute-tools',
    'version': '0.4.0',
    'description': "Utilities that make Ren'Py distribution less of a pain in the arse",
    'long_description': '# Ren\'Py Distribution Tools\n\nThe Ren\'Py Distribution Tools (RDT) is a set of utilities that make distribution of Ren\'Py projects easier and more seamless programmatically.\n\n[![MIT](https://img.shields.io/github/license/unscriptedvn/rdt)](LICENSE.txt)\n![Python](https://img.shields.io/badge/python-3.7+-blue.svg)\n[![PyPI version](https://badge.fury.io/py/renpy-distribute-tools.svg)](https://pypi.org/project/renpy-distribute-tools)\n\n## Getting Started\n\n### Quick Start: Install via PyPI/Poetry\n\nTo install via PyPI:\n\n```\npip install renpy-distribute-tools\n```\n\nOr, if you\'re using a Poetry project, just add the dependency:\n\n```\npoetry add renpy-distribute-tools\n```\n\n### Building from source\n\n#### Requirements\n\n- Python 3.7 or higher\n- Poetry package manager\n\nRen\'Py Distribute Tools is a Poetry project and can be built using Poetry\'s `build` command.\n\n1. Clone the repository.\n2. In the root of the project, run `poetry install`.\n3. Finally, run `poetry build`.\n\n## What\'s included\n\nThe Ren\'Py Distribution Tools set comes with utilities that make it easy to do the following:\n\n- Modifying a visual novel\'s `Info.plist`.\n- Code-signing the visual novel binaries in the Mac app with entitlements.\n- Creating a ZIP copy of the Mac app and sending it to Apple\'s notarization servers.\n- Verifying the notarization status of an app.\n- Stapling the notarization ticket to a macOS app.\n- Distributing app content through Itch.io.\n\n## Usage\n\nThe documentation website covers all of the modules contained in the RDT package. [View docs &rsaquo;](https://unscriptedvn.github.io/rdt/)\n\n### Example Usage: Notarizing a macOS build\n\n```py\nimport renpy_distribute_tools as rdt\n\nauthor = "Joe Smith"\nbundle_identifier = "com.example.my-vn"\ncode_sign_identity = "Developer ID Application: Joe Smith (XXXXXXXXXX)"\napp_path = "VN-1.0.0-dists/VN-1.0.0-mac/VN.app"\napple_email = "example.joesmith@icloud.com"\napple_provider = "XXXXXXXXXX"\n\nrdt.fix_plist(app_path + "/Contents/Info.plist",\n          bundle_identifier,\n          "\xc2\xa9 %s %s. All rights reserved." % (date.today().year, author))\nrdt.code_sign(code_sign_identity,\n          app_path,\n          entitlements="../../entitlements.plist",\n          enable_hardened_runtime=True)\ntry:\n    rdt.upload_to_notary(app_path,\n                     bundle_identifier,\n                     apple_email,\n                     "@keychain:AC_PASSWORD",\n                     provider=apple_provider)\nexcept CalledProcessError:\n    print("\\033[31;1mNotarization request failed. Aborting.\\033[0m")\n    sys.exit(1)\n```\n\n## License\n\nRDT is licensed under the MIT License, which is available in the LICENSE file in the source code repository.\n',
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UnscriptedVN/rdt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
