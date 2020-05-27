# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flirextractor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'pillow>=6.2,<=8.0.0', 'pyexiftool>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'flirextractor',
    'version': '1.0.1',
    'description': 'An efficient GPLv3-licensed Python package for extracting temperature data from FLIR IRT images.',
    'long_description': '# flirextractor\n\n<p align="center">\n<a href="https://pypi.org/project/flirextractor/"><img alt="PyPI" src="https://img.shields.io/pypi/v/flirextractor"></a>\n<a href="https://github.com/aloisklink/flirextractor/workflows/Tests/badge.svg"><img alt="GitHub Actions Status" src="https://github.com/aloisklink/flirextractor/workflows/Tests/badge.svg"></a>\n<a href="https://pypi.org/project/flirextractor/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/flirextractor"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://github.com/aloisklink/flirextractor/blob/master/LICENSE.md"><img alt="GitHub: License" src="https://img.shields.io/github/license/aloisklink/flirextractor"></a>\n</p>\n\nAn efficient GPLv3-licensed Python package for extracting temperature data from FLIR IRT images.\n\n## Differences from existing libraries\n\nThere is an existing Python package for extracting temperature\nvalues from raw IRT images, see\n[nationaldronesau/FlirImageExtractor](https://github.com/nationaldronesau/FlirImageExtractor).\nHowever, it has some issues that I didn\'t like:\n\n  - Most importantly, it is forked from the UNLICENSED\n    [Nervengift/read_thermal.py](https://github.com/Nervengift/read_thermal.py),\n    so until\n    [Nervengift/read_thermal.py#4](https://github.com/Nervengift/read_thermal.py/issues/4)\n    is answered, this package cannot be legally used.\n  - Secondly, it is quite inefficient, as it runs a new exiftool process\n    for each image, and it converts the temperature for each pixel, instead\n    of using numpy\'s vectorized math.\n\n## Installing\n\nYou can install flirextractor from pip.\n\n```bash\npip3 install flirextractor\n```\n\nOr, using the python package manger [poetry](https://poetry.eustace.io/)\n(recommended):\n\n```bash\npoetry add flirextractor\n```\n\n**Make sure you install exiftool as well.**\n\nOn RHEL, this can be installed via:\n\n```bash\nsudo yum install perl-Image-ExifTool\n```\n\nOn Debian, this can be installed via:\n\n```bash\nsudo apt update && sudo apt install libimage-exiftool-perl -y\n```\n\n## Usage\n\nEach FLIR infrared image is loaded in Celsius as a 2-dimensional\n[`numpy.ndarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).\n\nTo load data from a single FLIR file, run:\n\n```python3\nfrom flirextractor import FlirExtractor\nwith FlirExtractor() as extractor:\n    thermal_data = extractor.get_thermal("path/to/FLIRimage.jpg")\n```\n\nData can also be loaded from multiple FLIR files at once in batch mode,\nwhich is slightly more efficient:\n\n```python3\nfrom flirextractor import FlirExtractor\nwith FlirExtractor() as extractor:\n    list_of_thermal_data = extractor.get_thermal_batch(\n        ["path/to/FLIRimage.jpg", "path/to/another/FLIRimage.jpg"])\n```\n\nOnce you have the `numpy.ndarray`, you can export the data as a csv with:\n\n```python3\nimport numpy as np\nnp.savetxt("output.csv", thermal_data, delimiter=",")\n```\n\nYou can display the image for debugging by doing:\n\n```python3\nfrom PIL import Image\nthermal_image = Image.fromarray(thermal_data)\nthermal_image.show()\n```\n\nSee [./scripts/example.py](./scripts/example.py) for more example usage.\n\n## Testing\n\nUse the Python package manager `poetry` to install test dependencies:\n\n```bash\npoetry install\n```\n\nThen run pytest to run tests.\n\n```bash\npoetry run pytest\n```\n\nYou can run linters with pre-commit:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\n## Acknowledgements\n\nThis work was supported by the\nEngineering and Physical Sciences Research Council\n[Doctoral Training Partnership Grant EP/R513325/1].\n\nAdditionally, many thanks to Glenn J. Tattersall, for their\n[gtatters/Thermimage](https://github.com/gtatters/Thermimage) R package.\nThis work uses an image and adapts part of\n[gtatters/Thermimage](https://github.com/gtatters/Thermimage)\nunder the GPLv3.0 License.\n',
    'author': 'Alois Klink',
    'author_email': 'alois.klink@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aloisklink/flirextractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
