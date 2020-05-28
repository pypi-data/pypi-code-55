# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mcross', 'mcross.gui']

package_data = \
{'': ['*']}

install_requires = \
['curio>=1.2,<2.0']

entry_points = \
{'console_scripts': ['mcross = mcross:run']}

setup_kwargs = {
    'name': 'mcross',
    'version': '0.5.8',
    'description': 'Do you remember www?',
    'long_description': 'McRoss is a minimal and usable [gemini://](https://gemini.circumlunar.space/)\nbrowser written in python and tkinter, meaning it Just Works (tm) on any\nself-respecting desktop OS: Linux, Windows, Mac OS, and maybe the BSDs?\nNever tried one of those.\n\nIt currently looks like this:\n\n![](https://junk.imnhan.com/mcross.png)\n\nOr check out the demo video: https://junk.imnhan.com/mcross.mp4\n\nSurfing plaintext and gemini content is already working well.\nSee feature checklist below for more details.\n\n\n# Installation\n\n```sh\npip install mcross\nmcross\n```\n\nBetter distribution methods to be explored later.\nMaybe it\'s finally time to try nuitka?\n\n\n# Development\n\nDeps:\n\n- python3.7+\n- idlelib (it\'s supposed to be in the standard lib but Ubuntu for example\n  splits it into a separate package)\n- curio - for async I/O so that it doesn\'t block the UI.\n\nTo get started:\n\n```sh\npyenv install 3.7.7\npyenv virtualenv 3.7.7 mcross\npyenv activate\npoetry install\nmcross\n\n# to publish, first bump version in pyproject.toml then\npoetry publish --build\n```\n\n\n# Feature checklist\n\n- [x] back-forward buttons\n- [x] handle redirects\n- [x] non-blocking I/O using curio\n- [x] more visual indicators: waiting cursor, status bar\n- [x] parse gemini\'s advanced line types\n- [ ] TOFU TLS (right now it accepts whatever)\n- [ ] properly handle mime types (gemini/plaintext/binary)\n- [ ] configurable document styling\n- [ ] human-friendly distribution\n\nLong term high-level goals:\n\n## Easy for end users to install\n\nIf the words `cargo build` exists in the installation guide for your G U I\napplication then I\'m sorry it\'s not software made for people to _use_.\n\n## What-you-see-is-what-you-write\n\nA rendered text/gemini viewport should preserve its original text content.\nThis way once you\'ve read a gemini page on the browser, you already know how to\nwrite one. No "View Source" necessary.\n\n## Responsive & pleasant to use\n\nThe Castor browser doesn\'t have visual indicators at all, for example, when\nclicking on a link it just appears to do nothing until the new page is\ncompletely loaded. That is A Bad Thing (tm).\n\n## Lightweight\n\nIn terms of both disk space & memory/cpu usage.\nThe python/tkinter combo already puts us at a pretty good starting point.\n\n# Server bugs/surprises\n\n## Forces gemini:// in request\n\nSpec says protocol part is optional, but if I omit that one the server will\nrespond with `53 No proxying to other hosts!`.\n\n## Newline\n\nSpec says a newline should be \\r\\n but the server running\ngemini.circumlunar.space just uses \\n every time.\n',
    'author': 'nhanb',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~nhanb/mcross/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
