# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slskit']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=4.1.0,<5.0.0',
 'funcy>=1.14,<2.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pyyaml>=5.1,<6.0',
 'salt>=3000.2,<3001.0']

entry_points = \
{'console_scripts': ['slskit = slskit:run_module']}

setup_kwargs = {
    'name': 'slskit',
    'version': '2020.5.1',
    'description': 'Tools for checking Salt state validity',
    'long_description': '# slskit\n\n![release](https://img.shields.io/github/release/gediminasz/slskit.svg)\n![last commit](https://img.shields.io/github/last-commit/gediminasz/slskit.svg)\n![build](https://github.com/gediminasz/slskit/workflows/CI/badge.svg?branch=master)\n![black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n```\nusage: slskit [-h] [-V] [-c CONFIG]\n              {highstate,sls,pillars,refresh,snapshot} ...\n\nslskit - tools for checking Salt state validity\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         show program\'s version number and exit\n  -c CONFIG, --config CONFIG\n                        path to slskit configuration file (default:\n                        slskit.yaml or slskit.yml)\n\ncommands:\n  {highstate,sls,pillars,refresh,snapshot}\n    highstate           render highstate for specified minions\n    sls                 render a given sls for specified minions\n    pillars             render pillar items for specified minions\n    refresh             invoke saltutil.sync_all runner\n    snapshot            create and check highstate snapshots\n```\n\n---\n\n## Workaround for libcrypto.dylib failing to load on macOS\n\nIf `slskit` fails with `zsh: abort` or `Abort trap: 6`, inspect the error by running the command with `PYTHONDEVMODE=1`. If the issue is with `_load_libcrypto` call in `rsax931.py`, edit `salt/utils/rsax931.py` line 38:\n\n```diff\n-lib = find_library(\'crypto\')\n+lib = "/usr/local/opt/openssl@1.1/lib/libcrypto.dylib"\n```\n\nMore info:\n\n- https://github.com/saltstack/salt/issues/55084\n- https://github.com/Homebrew/homebrew-core/pull/45895/files#diff-5bdebf3b9146d50b15f9a0dc7e7def27R131-R133\n\n## Workaround for exception raised when processing __virtual__ function\n\nWhen seeing errors like these:\n\n```\nERROR:salt.loader:Exception raised when processing __virtual__ function for salt.loaded.int.module.freebsdkmod. Module will not be loaded: \'kernel\'\nWARNING:salt.loader:salt.loaded.int.module.freebsdkmod.__virtual__() is wrongly returning `None`. It should either return `True`, `False` or a new name. If you\'re the developer of the module \'freebsdkmod\', please fix this.\n```\n\nYou may need to add a corresponding grain to `slskit.yaml` file, e.g.:\n\n```yaml\n# slskit.yaml\n\nslskit:\n  roster:\n    foo:\n      grains:\n        kernel: Linux\n```\n\nYou can find values for grains by inspecting `grains.items` on your real minions.\n\n## How to keep your grains DRY\n\nUse `default_grains` option to avoid duplicating the same grains over all minions:\n\n```yaml\n# slskit.yaml\n\nslskit:\n  roster:\n    foo:\n    bar:\n    baz:\n  default_grains:\n    os: Ubuntu\n```\n\nFor more advanced cases use YAML anchors:\n\n```yaml\n# slskit.yaml\n\n_grains:\n  ubuntu: &ubuntu\n    os: Ubuntu\n  fedora: &fedora\n    os: Fedora\n\nslskit:\n  roster:\n    u1:\n      grains:\n        <<: *ubuntu\n    u2:\n      grains:\n        <<: *ubuntu\n    f1:\n      grains:\n        <<: *fedora\n    f2:\n      grains:\n        <<: *fedora\n```\n',
    'author': 'Gediminas Zlatkus',
    'author_email': 'gediminas.zlatkus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gediminasz/slskit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
