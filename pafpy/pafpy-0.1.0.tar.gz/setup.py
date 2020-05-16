# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pafpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pafpy',
    'version': '0.1.0',
    'description': 'A lightweight library for working with PAF (Pairwise mApping Format) files',
    'long_description': '# pafpy\n\nA lightweight library for working with [PAF][PAF] (Pairwise mApping Format) files.\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mbhall88/pafpy/Python_package)](https://github.com/mbhall88/pafpy/actions)\n[![codecov](https://codecov.io/gh/mbhall88/pafpy/branch/master/graph/badge.svg)](https://codecov.io/gh/mbhall88/pafpy)\n[![PyPI](https://img.shields.io/pypi/v/pafpy)](https://pypi.org/project/pafpy/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pafpy)\n![License](https://img.shields.io/github/license/mbhall88/pafpy)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Documentation**: <https://pafpy.xyz>\n\n[TOC]: #\n\n# Table of Contents\n- [Install](#install)\n  - [PyPi](#pypi)\n  - [Conda](#conda)\n  - [Locally](#locally)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n\n## Install\n\n### PyPi\n\n```sh\npip install pafpy\n```\n\n### Conda\n\n```sh\nconda install -c bioconda pafpy\n```\n\n### Locally\n\nIf you would like to install locally, the recommended way is using [poetry][poetry].\n\n```sh\ngit clone https://github.com/mbhall88/pafpy.git\ncd pafpy\nmake install\n# to check the library is installed run\npoetry run python -c "from pafpy import PafRecord;print(str(PafRecord()))"\n# you should see a (unmapped) PAF record printed to the terminal\n# you can also run the tests if you like\nmake test-code\n```\n\n## Usage\n\nFor full usage, please refer to the [documentation][docs]. If there is any functionality\nyou feel is missing or would make `pafpy` more user-friendly, please raise an issue\nwith a feature request.\n\nIn the below basic usage pattern, we collect the [BLAST identity][blast] of all primary\nalignments in our PAF file into a list.\n\n```py\nfrom typing import List\nfrom pafpy import PafFile\n\npath = "path/to/sample.paf"\n\nidentities: List[float] = []\nwith PafFile(path) as paf:\n    for record in paf:\n        if record.is_primary():\n            identity = record.blast_identity()\n            identities.append(identity)\n```\n\nAnother use case might be that we want to get the identifiers of all records aligned to\na specific contig, but only keep the alignments where more than 50% of the query (read)\nis aligned.\n\n```py\nfrom typing import List\nfrom pafpy import PafFile\n\npath = "path/to/sample.paf"\n\ncontig = "chr1"\nmin_covg = 0.5\nidentifiers: List[str] = []\nwith PafFile(path) as paf:\n    for record in paf:\n        if record.tname == contig and record.query_coverage > min_covg:\n            identifiers.append(record.qname)\n```\n\n## Contributing\n\nIf you would like to contribute to `pafpy`, checkout [`CONTRIBUTING.md`][contribute].\n\n[poetry]: https://python-poetry.org/\n[PAF]: https://github.com/lh3/miniasm/blob/master/PAF.md\n[docs]: https://pafpy.xyz/\n[blast]: https://lh3.github.io/2018/11/25/on-the-definition-of-sequence-identity#blast-identity\n[contribute]: https://github.com/mbhall88/pafpy/blob/master/CONTRIBUTING.md\n\n',
    'author': 'Michael Hall',
    'author_email': 'michael@mbh.sh',
    'maintainer': 'Michael Hall',
    'maintainer_email': 'michael@mbh.sh',
    'url': 'https://github.com/mbhall88/pafpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
