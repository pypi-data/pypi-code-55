# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deethon']

package_data = \
{'': ['*']}

install_requires = \
['mutagen>=1.44.0,<2.0.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'deethon',
    'version': '0.3.1',
    'description': 'Python3 library to easily download music from Deezer',
    'long_description': 'Deethon\n=======\nPython3 library to easily download music from `Deezer`_.\n\nQuickstart\n----------\nInstalling\n^^^^^^^^^^\n.. code-block:: sh\n\n    pip3 install deethon\n\nInitialize\n^^^^^^^^^^\n.. code-block:: python\n\n    import deethon\n\n    deezer = deethon.Session("DEEZER ARL TOKEN")\n\nDownload tracks\n^^^^^^^^^^^^^^^\nDownload track by Deezer link\n\n.. code-block:: python\n\n    deezer.download(\n        "Deezer track url",\n        bitrate="FLAC" # MP3_320 / MP3_256 / MP3_128 (optional)\n    )\n\nDisclaimer\n----------\n| Deethon - Python3 library to download music from Deezer\n| Copyright (C) 2020  Aykut Yilmaz\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see https://www.gnu.org/licenses/.\n\nDo not use this package illegaly and against Deezer\'s `Terms Of Use`_.\n\n.. _Deezer: https://www.deezer.com\n.. _Terms Of Use: https://www.deezer.com/legal/cgu/',
    'author': 'Aykut Yilmaz',
    'author_email': 'aykuxt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deethon/deethon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
