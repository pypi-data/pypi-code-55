# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcdc']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'codetiming>=1.2.0,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'py-cpuinfo>=5.0.0,<6.0.0']

extras_require = \
{'cython': ['cython>=0.29,<0.30']}

entry_points = \
{'console_scripts': ['fastcdc = fastcdc.cli:cli']}

setup_kwargs = {
    'name': 'fastcdc',
    'version': '1.2.0',
    'description': 'FastCDC (content defined chunking) in pure Python.',
    'long_description': '# FastCDC\n\n[![Tests](https://github.com/titusz/fastcdc-py/workflows/Tests/badge.svg)](https://github.com/titusz/fastcdc-py/actions?query=workflow%3ATests)\n[![Version](https://img.shields.io/pypi/v/fastcdc.svg)](https://pypi.python.org/pypi/fastcdc/)\n[![Downloads](https://pepy.tech/badge/fastcdc)](https://pepy.tech/project/fastcdc)\n\nThis package implements the "FastCDC" content defined chunking algorithm in pure\nPython. A critical aspect of its behavior is that it returns exactly the same\nresults for the same input. To learn more about content defined chunking and its\napplications, see the reference material linked below.\n\n\n## Requirements\n\n* [Python](https://www.python.org/) Version 3.6 and later.\n\n## Installing\n\n```shell\n$ pip3 install fastcdc\n```\n\n## Example Usage\n\nAn example can be found in the `examples` directory of the source repository,\nwhich demonstrates reading files of arbitrary size into a memory-mapped buffer\nand passing them through the chunker (and computing the SHA256 hash digest of\neach chunk).\n\n### Calculate chunks with default settings:\n```shell\n$ fastcdc tests/SekienAkashita.jpg\nhash=103159aa68bb1ea98f64248c647b8fe9a303365d80cb63974a73bba8bc3167d7 offset=0 size=22366\nhash=3f2b58dc77982e763e75db76c4205aaab4e18ff8929e298ca5c58500fee5530d offset=22366 size=10491\nhash=fcfb2f49ccb2640887a74fad1fb8a32368b5461a9dccc28f29ddb896b489b913 offset=32857 size=14094\nhash=bd1198535cdb87c5571378db08b6e886daf810873f5d77000a54795409464138 offset=46951 size=18696\nhash=d6347a2e5bf586d42f2d80559d4f4a2bf160dce8f77eede023ad2314856f3086 offset=65647 size=43819\n```\n\n### Customize min-size, avg-size, max-size, and hash function\n```shell\n$ fastcdc -mi 16384 -s 32768 -ma 65536 -hf sha256 tests/SekienAkashita.jpg\nhash=5a80871bad4588c7278d39707fe68b8b174b1aa54c59169d3c2c72f1e16ef46d offset=0 size=32857\nhash=13f6a4c6d42df2b76c138c13e86e1379c203445055c2b5f043a5f6c291fa520d offset=32857 size=16408\nhash=0fe7305ba21a5a5ca9f89962c5a6f3e29cd3e2b36f00e565858e0012e5f8df36 offset=49265 size=60201\n```\n\n### Show help\n\n```shell\n$ fastcdc -h\nUsage: fastcdc [OPTIONS] FILE\n\n  Splits a (large) file into variable sized chunks and computes hashes.\n\nOptions:\n  --version                  Show the version and exit.\n  -s, --size INTEGER         The desired average size of the chunks.\n                             [default: 16384]\n\n  -mi, --min-size INTEGER    Minimum chunk size (default size/4)\n  -ma, --max-size INTEGER    Maximum chunk size (default size*8)\n  -hf, --hash-function TEXT  [default: sha256]\n  --help                     Show this message and exit.\n```\n\n### Use from your python code\nThe  tests also have some short examples of using the chunker, of which this\ncode snippet is an example:\n\n```python\nfrom fastcdc import fastcdc\n\nresults = list(fastcdc("tests/SekienAkashita.jpg", 16384, 32768, 65536))\nassert len(results) == 3\nassert results[0].offset == 0\nassert results[0].length == 32857\nassert results[1].offset == 32857\nassert results[1].length == 16408\nassert results[2].offset == 49265\nassert results[2].length == 60201\n```\n\n## Reference Material\n\nThe algorithm is as described in "FastCDC: a Fast and Efficient Content-Defined\nChunking Approach for Data Deduplication"; see the\n[paper](https://www.usenix.org/system/files/conference/atc16/atc16-paper-xia.pdf),\nand\n[presentation](https://www.usenix.org/sites/default/files/conference/protected-files/atc16_slides_xia.pdf)\nfor details. There are some minor differences, as described below.\n\n### Differences with the FastCDC paper\n\nThe explanation below is copied from\n[ronomon/deduplication](https://github.com/ronomon/deduplication) since this\ncodebase is little more than a translation of that implementation:\n\n> The following optimizations and variations on FastCDC are involved in the chunking algorithm:\n> * 31 bit integers to avoid 64 bit integers for the sake of the Javascript reference implementation.\n> * A right shift instead of a left shift to remove the need for an additional modulus operator, which would otherwise have been necessary to prevent overflow.\n> * Masks are no longer zero-padded since a right shift is used instead of a left shift.\n> * A more adaptive threshold based on a combination of average and minimum chunk size (rather than just average chunk size) to decide the pivot point at which to switch masks. A larger minimum chunk size now switches from the strict mask to the eager mask earlier.\n> * Masks use 1 bit of chunk size normalization instead of 2 bits of chunk size normalization.\n\nThe primary objective of this codebase was to have a Python implementation with a\npermissive license, which could be used for new projects, without concern for\ndata parity with existing implementations.\n\n## Prior Art\n\nThis crate is little more than a rewrite of the implementation by Joran Dirk\nGreef (see the ronomon link below), in Rust, and greatly simplified in usage.\nOne significant difference is that the chunker in this crate does _not_\ncalculate a hash digest of the chunks.\n\n* [nlfiedler/fastcdc-rs](https://github.com/nlfiedler/fastcdc-rs)\n    + Rust implementation on which this code is based.\n* [ronomon/deduplication](https://github.com/ronomon/deduplication)\n    + C++ and JavaScript implementation on which the rust implementation is based.\n* [rdedup_cdc at docs.rs](https://docs.rs/crate/rdedup-cdc/0.1.0/source/src/fastcdc.rs)\n    + An alternative implementation of FastCDC to the one in this crate.\n* [jrobhoward/quickcdc](https://github.com/jrobhoward/quickcdc)\n    + Similar but slightly earlier algorithm by some of the same researchers.\n\n## Change Log\n\n## [1.2.0] - 2020-05-23\n\n### Added\n- faster optional cython implementation\n- benchmark command\n\n## [1.1.0] - 2020-05-09\n\n### Added\n- high-level API\n- support for streams\n- support for custom hash functions\n\n\n## [1.0.0] - 2020-05-07\n\n### Added\n- Initial release (port of [nlfiedler/fastcdc-rs](https://github.com/nlfiedler/fastcdc-rs)).\n\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iscc/fastcdc-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
