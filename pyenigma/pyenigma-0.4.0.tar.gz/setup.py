# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyenigma']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['enigma = bin.enigma:main']}

setup_kwargs = {
    'name': 'pyenigma',
    'version': '0.4.0',
    'description': 'Python Enigma cypher machine simulator.',
    'long_description': '# pyEnigma\n\n[![builds.sr.ht status](https://builds.sr.ht/~cedric/pyenigma.svg)](https://builds.sr.ht/~cedric/pyenigma)\n\n\n[pyEnigma](https://sr.ht/~cedric/pyenigma) is a  Python Enigma cypher machine\nsimulator.\n\nFor reporting issues, visit the tracker here:\nhttps://todo.sr.ht/~cedric/pyenigma\n\n\n## Usage\n\n\n### As a Python library\n\nYou can install pyEnigma with Poetry.\n\n```bash\n$ poetry install pyenigma\n```\n\nThen you can use it in your program:\n\n```bash\n$ poetry shell\n(pyenigma-X0xzv6Ge-py3.8) $\n(pyenigma-X0xzv6Ge-py3.8) $ python\n```\n\n```python\nPython 3.8.0 (default, Dec 11 2019, 21:43:13)\n[GCC 9.2.1 20191008] on linux\nType "help", "copyright", "credits" or "license" for more information.\n>>> from pyenigma import enigma\n>>> from pyenigma import rotor\n>>> print(rotor.ROTOR_GR_III)\n\n    Name: III\n    Model: German Railway (Rocket)\n    Date: 7 February 1941\n    Wiring: JVIUBHTCDYAKEQZPOSGXNRMWFL\n>>>\n>>> engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,\n                                rotor.ROTOR_II, rotor.ROTOR_III, key="ABC",\n                                plugs="AV BS CG DL FU HZ IN KM OW RX")\n>>> print(engine)\n\n    Reflector:\n    Name: Reflector A\n    Model: None\n    Date: None\n    Wiring: EJMZALYXVBWFCRQUONTSPIKHGD\n\n    Rotor 1:\n    Name: I\n    Model: Enigma 1\n    Date: 1930\n    Wiring: EKMFLGDQVZNTOWYHXUSPAIBRCJ\n    State: A\n\n    Rotor 2:\n    Name: II\n    Model: Enigma 1\n    Date: 1930\n    Wiring: AJDKSIRUXBLHWTMCQGZNPYFVOE\n    State: B\n\n    Rotor 3:\n    Name: III\n    Model: Enigma 1\n    Date: 1930\n    Wiring: BDFHJLCPRTXVZNYEIWGAKMUSQO\n    State: C\n>>> secret = engine.encipher("Hello World")\n>>> print(secret)\nQgqop Vyzxp\n```\n\n### As a program\n\nInstall pyEnigma system wide with pipx:\n\n```bash\n$ pipx install pyenigma\n```\n\nThen you can use the command line interface:\n\n```bash\n$ echo "Hello World" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"\nQgqop Vyzxp\n\n$ echo "Qgqop Vyzxp" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"\nHello World\n```\n\nIf you want to display the rotor output state:\n\n```bash\n$ echo "Hello World" | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX" --verbose\nQgqop Vyzxp\nKBC A I II III "AV BS CG DL FU HZ IN KM OW RX"\n```\n\nThe state is returned on ```stderr```, so you can still use the Unix pipe mechanism:\n\n```bash\n$ echo "Hello World" | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX" --verbose | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX"\nKBC A I II III "AV BS CG DL FU HZ IN KM OW RX"\nHello World\n```\n\n\n## License\n\npyEnigma is licensed under\n[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.html)\n\n\n## Author\n\n* [Christophe Goessen](https://github.com/cgoessen) (initial author)\n* [Cédric Bonhomme](https://www.cedricbonhomme.org)\n',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~cedric/pyenigma',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
