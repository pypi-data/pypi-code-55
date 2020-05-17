# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['despoilerizer']

package_data = \
{'': ['*']}

install_requires = \
['click']

setup_kwargs = {
    'name': 'despoilerizer',
    'version': '1.0.1',
    'description': 'Remove spoilers from files.',
    'long_description': '# Despoilerizer\n\nThis script reads from stdin and prints out the contents of stdin to stdout,\nwithout the lines that are in between the `:SPOILERS BEGIN:` and the\n`:SPOILERS END:` tags.\n\nIt uses stdin and stdout so that it can be easily integrated in bash \nscripting, for instance:\n```bash\n$ <my_file.tex | python -m despoilerizer | pdflatex\n```\n\nYou can also redefine the tags:\n\n```bash\n$ <my_file.tex | \\\n  python -m despoilerizer --begin="# spoiler" --end="# unspoiler" | \\\n  pdflatex\n```\n\n## Installation\n\n```bash\n$ pip install despoilerizer\n```\n\n## Examples\n\n#### stdin\n```\nThis is a simple file.\n:SPOILERS BEGIN:\nIt contains spoilers.\n:SPOILERS END:\nAnd also other information.\n```\n\n#### stdout\n```\nThis is a simple file.\nAnd also other information.\n```\n\n#### stdin\n```\n\\begin{document}\n% :SPOILERS BEGIN:\nimportant stuff...\n% :SPOILERS END:\n\\end{document}\n```\n\n#### stdout\n```\n\\begin{document}\n\\end{document}\n```\n\n## Usage as importable package\n\n```python\nimport despoilerizer\nfrom pathlib import Path as P\n\nfor path in [P(\'file1.tex\'), P(\'file2.py\'), P(\'file3.txt\')]:\n    out_path = P(path.stem + \'_nospoilers\' + path.suffix)\n    with open(path, \'r\') as fin:\n        with open(out_path, \'w\') as fout:\n            despoilerizer.despoilerize_file(fin, fout)\n\n\ncontents = """\nThis is a very important string.\nsuch spoilers\nI really don\'t want anyone to know.\nmuch wow\n"""\n\nwith open(P(\'some_file.txt\'), \'w\') as f:\n    f.write(\n        despoilerizer.despoilerize(contents, begin=\'such spoilers\', end=\'much wow\')\n    )\n```\n\n## Motivation\n\nI have a LaTeX file for a document I\'m sharing with my friends.\nThis document contains some information for a DnD campaign both for stuff the \nplayers have encountered and stuff that\'s being worked on.\n\nTherefore, I want to have two different PDF documents: one with the spoilers\nand one without them.\n',
    'author': 'Daniele Parmeggiani',
    'author_email': 'git@danieleparmeggiani.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dpdani/despoilerizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
