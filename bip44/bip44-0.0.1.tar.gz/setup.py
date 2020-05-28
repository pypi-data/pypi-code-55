# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bip44']

package_data = \
{'': ['*']}

install_requires = \
['bip32>=0.0.7,<0.0.8', 'mnemonic>=0.19,<0.20', 'pysha3>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'bip44',
    'version': '0.0.1',
    'description': 'Simple python bip44 implementation. Mnemonic + bip32.',
    'long_description': '# python-bip44\n\nSimple python bip44 implementation. Mnemonic + bip32.\n\n## Install\n`pip install bip44`\n\n## Quick Start\n```python\n>>> from coincurve import PrivateKey\n>>> from bip44.wallet import Wallet\n>>> from bip44.utils import get_eth_addr\n>>> mnemonic = "purity tunnel grid error scout long fruit false embody caught skin gate"\n>>> w = Wallet(mnemonic)\n>>> sk, pk = w.derive_account("eth", account=0)\n>>> sk = PrivateKey(sk)\n>>> sk.public_key.format() == pk\nTrue\n>>> get_eth_addr(pk)\n\'0x7ad23d6ed9a1d98e240988bed0d78e8c81ec296c\'\n```\n',
    'author': 'Weiliang Li',
    'author_email': 'to.be.impressive@gmail.com',
    'maintainer': 'Weiliang Li',
    'maintainer_email': 'to.be.impressive@gmail.com',
    'url': 'https://github.com/kigawas/python-bip44',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
