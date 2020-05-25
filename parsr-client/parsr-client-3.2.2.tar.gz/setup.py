# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parsr_client']

package_data = \
{'': ['*']}

install_requires = \
['diff_match_patch>=20181111,<20181112',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'semver>=2.9.1,<3.0.0',
 'sxsdiff>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'parsr-client',
    'version': '3.2.2',
    'description': 'Python client for Parsr - Transforms PDF, Documents and Images into Enriched Structured Data',
    'long_description': "# Parsr Client\n\nProvides a python interface to the Parsr tool via its API.\nParsr transforms PDF, documents and images into enriched, structured data.\n\nFind out all about Parsr (including download) at [http://par.sr](http://par.sr).\n\n## 1 Installation\n\n```sh\npip install parsr\n```\n\n## 2 Usage\n\n_Make sure that the Parsr Server is already running. Let us suppose that the address is `localhost:3001`_\n\n### 2.1 Connect to the Parsr server\n\n```python\nfrom parsr_client import ParsrClient\nparsr = ParsrClient('localhost:3001')\n```\n\n### 2.2 Send the document\n\n```python\nparsr.send_document(\n   file_path='README.pdf',\n   config_path='defaultConfig.json'\n   document_name='The Readme',\n   save_request_id=True)\n```\n\n### 2.4 Retrieve results\n\n1. Get everything as a JSON:\n\n    ```python\n    parsr.get_json()\n    ```\n\n2. As Markdown:\n\n    ```python\n    parsr.get_markdown()\n    ```\n\n3. As text:\n\n    ```python\n    parsr.get_text()\n    ```\n\n4. Get the first table on the first page:\n\n    ```python\n    parsr.get_table(\n        page=1,\n        table=1,\n    )\n    ```\n\n5. Get all the versions of the document:\n\n    ```python\n    parsr.get_revisions('The Readme')\n    ```\n\n6. Get pretty diffs between each successive pair of a document's revisions:\n\n    ```python\n    parsr.compare_revisions('The Readme', pretty_html=True)\n    ```\n\n## 3 Interpreting the whole JSON output locally\n\nThe supplied `ParsrOutputInterpreter` class can be used to interpret the downloaded JSON output and generate higher level structures like the text body.\n\nHere's an example to generate text body on the first page from the above example.\n\n``` python\nfrom parsr_client import ParsrOutputInterpreter\n\nparsr_interpreter = ParsrOutputInterpreter(\n    parsr.get_json()\n)\n\nt = parsr_interpreter.get_text(\n    page_number=1\n)\nprint(t)\n```\n",
    'author': 'AXA Group Operations S.A.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://par.sr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
