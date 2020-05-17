# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfgen']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'syncasync>=20180812,<20180813']

entry_points = \
{'console_scripts': ['pdfgen-setup = pdfgen.setup:main']}

setup_kwargs = {
    'name': 'pdfgen',
    'version': '1.0.3',
    'description': 'Pyppeteer-based async python wrapper to convert html to pdf',
    'long_description': '# PDFGen-Python: HTML to PDF wrapper\n\n[![Build Status](https://travis-ci.org/shivanshs9/pdfgen-python.svg?branch=master)](https://travis-ci.org/shivanshs9/pdfgen-python) [![PyPI version](https://badge.fury.io/py/pdfgen.svg)](https://badge.fury.io/py/pdfgen) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/pdfgen.svg)](https://pypi.python.org/pypi/pdfgen/)\n\nPython 3.6.1+ async wrapper for [Pyppeteer](https://pyppeteer.github.io/pyppeteer/index.html) to convert HTML to PDF.\n\n**NOTE:** All the public API functions are adapted to async coroutines, so use them with await!\n\n---\n\nThis is adapted version of [python-PDFKit](https://github.com/JazzCore/python-pdfkit/) library, so big thanks to\nthem!\n\n---\n\n## Installation\n\n- Install pdfgen:\n\n```bash\n$ pip install pdfgen\n```\n\n- To download Chromium beforehand, run `$ pdfgen-setup`. Otherwise, it\'ll be downloaded on the first run of library.\n\n# Usage\n\nFor simple async tasks:\n\n```python\nimport pdfgen\n\nasync def f():\n    await pdfgen.from_url(\'http://google.com\', \'out.pdf\')\n    await pdfgen.from_file(\'test.html\', \'out.pdf\')\n    await pdfgen.from_string(\'Hello!\', \'out.pdf\')\n```\n\nSync API is also provided at `pdfgen.sync` for all the above-mentioned functions:\n\n```python\nimport pdfgen\n\npdfgen.sync.from_url(\'http://google.com\', \'out.pdf\')\npdfgen.sync.from_file(\'test.html\', \'out.pdf\')\npdfgen.sync.from_string(\'Hello!\', \'out.pdf\')\n```\n\nYou can pass a list with multiple URLs or files:\n\n```python\npdfgen.sync.from_url([\'google.com\', \'yandex.ru\', \'engadget.com\'], \'out.pdf\')\npdfgen.sync.from_file([\'file1.html\', \'file2.html\'], \'out.pdf\')\n```\n\nAlso you can pass an opened file:\n\n```python\nwith open(\'file.html\') as f:\n    pdfgen.sync.pdfgen(f, \'out.pdf\')\n```\n\nIf you wish to further process generated PDF, you can read it to a\nvariable:\n\n```python\n# Ignore output_path parameter to save pdf to a variable\npdf = pdfgen.sync.from_url(\'http://google.com\')\n```\n\nYou can specify all [Pyppeteer\noptions](https://pyppeteer.github.io/pyppeteer/reference.html#pyppeteer.page.Page.pdf) used for saving PDF as shown below:\n\n```python\noptions = {\n    \'scale\': 2.0,\n    \'format\': \'Letter\',\n    \'margin\': {\n        \'top\': \'0.75in\',\n        \'right\': \'0.75in\',\n        \'bottom\': \'0.75in\',\n        \'left\': \'0.75in\',\n    },\n    \'pageRanges\': \'1-5,8\',\n}\n\npdfgen.sync.from_url(\'http://google.com\', \'out.pdf\', options=options)\n```\n\nYou can also pass any options through meta tags in your HTML:\n\n```python\nbody = """\n    <html>\n      <head>\n        <meta name="pdfgen-format" content="Legal"/>\n        <meta name="pdfgen-landscape" content="False"/>\n      </head>\n      Hello World!\n      </html>\n    """\n\npdfgen.sync.from_string(body, \'out.pdf\')\n```\n\n## Configuration\n\nEach API call takes an optional options parameter to configure print PDF behavior. However, to reduce redundancy, one can certainly set default configuration to be used for all API calls. It takes the\nconfiguration options as initial paramaters. The available options are:\n\n- `options` - the dict used by default for pyppeteer `page.pdf(options)` call. `options` passed as argument to API call will take precedence over the default options.\n- `meta_tag_prefix` - the prefix for `pdfgen` specific meta tags - by\n  default this is `pdfgen-`.\n- `environ` - the dict used to provide env variables to pyppeteer headless browser.\n\n```python\nimport pdfgen\n\npdfgen.configuration(options={\'format\': \'A4\'})\n\nasync def f():\n    # The resultant PDF at \'output_file\' will be in A4 size and 2.0 scale.\n    await pdfgen.from_string(html_string, output_file, options={\'scale\': 2.0})\n```\n\n# Troubleshooting\n\n- `InvalidSourceError`:\n  Provided HTML source is invalid (maybe wrong URL or non-existing file)\n',
    'author': 'Shivansh Saini',
    'author_email': 'shivanshs9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shivanshs9/pdfgen-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
