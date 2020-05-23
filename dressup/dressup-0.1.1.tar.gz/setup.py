# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dressup']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'rich>=1.2.2,<2.0.0',
 'toml>=0.10.1,<0.11.0',
 'typer>=0.1.1,<0.3.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['dressup = dressup.console:app']}

setup_kwargs = {
    'name': 'dressup',
    'version': '0.1.1',
    'description': 'Dress up',
    'long_description': '# Dress up\n\n![Dress up logo](docs/images/logo.png)\n\n[![Tests](https://github.com/pscosta5/dressup/workflows/Tests/badge.svg)](https://github.com/pscosta5/dressup/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/pscosta5/dressup/branch/master/graph/badge.svg)](https://codecov.io/gh/pscosta5/dressup)\n[![PyPI](https://img.shields.io/pypi/v/dressup.svg)](https://pypi.org/project/dressup/)\n[![Python Version](https://img.shields.io/pypi/pyversions/dressup)](https://pypi.org/project/dressup)\n[![Read the Docs](https://readthedocs.org/projects/dressup/badge/)](https://dressup.readthedocs.io/)\n[![License](https://img.shields.io/pypi/l/dressup)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nConvert your strings to various Unicode characters. Turn "words" into "𝔴𝔬𝔯𝔡𝔰", "🆆🅾🆁🅳🆂",\nand "𝔀𝓸𝓻𝓭𝓼".\n\n![usage animation](docs/images/usage.gif)\n\n---\n\n**Documentation:**\n[https://dressup.readthedocs.io/](https://dressup.readthedocs.io/en/latest/)\n\n---\n\n## Contents\n\n1. [**Installation**](#installation)\n2. [**Usage**](#usage)\n   - [**Command-line**](#command-line-usage)\n   - [**Library**](#library-usage)\n3. [**Contributing**](#contributing)\n\n## Installation\n\nTo install Dress up, run this command in your terminal\n\n```sh\n❯ python -m pip install dressup\n```\n\nIf you\'re using it primarily as a command-line tool, it\'s recommended you install it via\n[pipx](https://github.com/pipxproject/pipx)\n\n```sh\n❯ pipx install dressup\n```\n\n## Usage\n\nThere are two primary ways to use Dress up—as a command-line tool, or as Python library.\n\n### Command-line usage\n\nDisplay all possible transformations by running:\n\n```sh\n❯ dressup Hello\nCircle\n\nⒽⓔⓛⓛⓞ\n\nNegative circle\n\n🅗🅔🅛🅛🅞\n\nMonospace\n\nＨｅｌｌｏ\n\nMath bold\n\n𝐇𝐞𝐥𝐥𝐨\n\n...\n```\n\nReturn only a specific transformation by using the `--type` flag.\n\n```sh\n❯ dressup Vibes --type inverted\n𐌡ıqǝs\n```\n\n#### Autocompletion\n\n![autocompletion animation](docs/images/autocompletion.gif)\n\nDress up supports argument completions along with live previews. To enable\nautocompletion run.\n\n```sh\n❯ dressup --install-completion zsh\nzsh completion installed in /Users/username/.zshrc.\n```\n\nCompletion will take effect once you restart the terminal.\n\n`zsh` may be replaced with `bash`, `fish`, `powershell`, or `pwsh`. Along with typical\nautocompletion, when typing in a value for `--type` if `[TAB]` is pressed the matching\nparameter values will be displayed below along with a preview of the conversion.\n\n```sh\n❯ dressup Words --type math [TAB]\nmath-bold              -- 𝐖𝐨𝐫𝐝𝐬\nmath-bold-fraktur      -- 𝖂𝖔𝖗𝖉𝖘\nmath-bold-italic       -- 𝑾𝒐𝒓𝒅𝒔\nmath-bold-script       -- 𝓦𝓸𝓻𝓭𝓼\nmath-double-struck     -- 𝕎𝕠𝕣𝕕𝕤\nmath-fraktur           -- 𝔚𝔬𝔯𝔡𝔰\nmath-monospace         -- 𝚆𝚘𝚛𝚍𝚜\nmath-sans              -- 𝖶𝗈𝗋𝖽𝗌\nmath-sans-bold         -- 𝗪𝗼𝗿𝗱𝘀\nmath-sans-bold-italic  -- 𝙒𝙤𝙧𝙙𝙨\nmath-sans-italic       -- 𝘞𝘰𝘳𝘥𝘴\n```\n\n## Library usage\n\nTo convert characters, use `convert`.\n\n```python\nimport dressup\n\ndressup.convert("Hello", unicode_type="negative circle")\n```\n\n```sh\n\'🅗🅔🅛🅛🅞\'\n```\n\nTo return all possible conversions, use `show_all`.\n\n```python\nimport dressup\n\ndressup.show_all("Hello")\n```\n\n```sh\n{\'Circle\': \'Ⓗⓔⓛⓛⓞ\', \'Negative circle\': \'🅗🅔🅛🅛🅞\',\n\'Monospace\': \'Ｈｅｌｌｏ\', \'Math bold\': \'𝐇𝐞𝐥𝐥𝐨\',\n\'Math bold fraktur\': \'𝕳𝖊𝖑𝖑𝖔\', \'Math bold italic\': \'𝑯𝒆𝒍𝒍𝒐\',\n\'Math bold script\': \'𝓗𝓮𝓵𝓵𝓸\', \'Math double struck\': \'ℍ𝕖𝕝𝕝𝕠\',\n\'Math monospace\': \'𝙷𝚎𝚕𝚕𝚘\', \'Math sans\': \'𝖧𝖾𝗅𝗅𝗈\', \'Math sans bold\':\n\'𝗛𝗲𝗹𝗹𝗼\', \'Math sans bold italic\': \'𝙃𝙚𝙡𝙡𝙤\', \'Math sans italic\':\n\'𝘏𝘦𝘭𝘭𝘰\', \'Parenthesized\': \'⒣⒠⒧⒧⒪\', \'Square\': \'🄷🄴🄻🄻🄾\',\n\'Negative square\': \'🅷🅴🅻🅻🅾\', \'Cute\': \'Héĺĺő\', \'Math fraktur\':\n\'ℌ𝔢𝔩𝔩𝔬\', \'Rock dots\': \'Ḧëḷḷö\', \'Small caps\': \'ʜᴇʟʟᴏ\', \'Stroked\':\n\'Ħɇłłø\', \'Subscript\': \'ₕₑₗₗₒ\', \'Superscript\': \'ᴴᵉˡˡᵒ\',\n\'Inverted\': \'ɥǝןןo\', \'Reversed\': \'Hɘ⅃⅃o\'}\n```\n\n## Contributing\n\nAll character mappings are stored in [translator.toml](src/dressup/translator.toml).\nWant to add a new mapping or tweak an existing one? Simply edit\n[translator.toml](src/dressup/translator.toml) and create a pull request.\n\nCheck out [CONTRIBUTING.md](CONTRIBUTING.md) for general contribution guidelines.\n',
    'author': 'Paulo S. Costa',
    'author_email': 'Paulo.S.Costa.5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pscosta5/dressup',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
