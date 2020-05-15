# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gecos']

package_data = \
{'': ['*']}

install_requires = \
['biotite>=0.21', 'numpy>=1.13,<2.0', 'scikit-image>=0.17']

entry_points = \
{'console_scripts': ['gecos = gecos.cli:main']}

setup_kwargs = {
    'name': 'gecos',
    'version': '1.2.0',
    'description': 'Generated color schemes for sequence alignment visualizations',
    'long_description': 'Gecos - Generated Color Schemes for sequence alignment visualizations\n=====================================================================\n\nMultiple sequence alignments are often visualized by coloring the symbols\naccording to some kind of properties.\nFor example a color scheme for amino acids could use one color for\nhydrophobic residues, another color for positively charged residues\nand so forth.\nUsually, such color schemes are manually created by experienced people\nwho have knowledge about the characteristics of the e.g. amino acids,\nso they can assign equal or similar colors to amino acids that share\nsimilar properties.\n\nThe *Gecos* software follows a different approach:\nInstead of looking at specific, sometimes subjective properties,\nit uses another source for estimating the similarity of symbols:\nthe substitution matrix itself.\nSimilar colors are assigned to high scoring pairs of symbols, low\nscoring pairs get distant colors - in a completely automatic manner.\nAs a result the distance of two symbols in the substitution matrix corresponds\nto the perceptual differences in the color scheme.\n\nHow about an example?\nThe following command line invocation creates a light color scheme.\nAn example alignment using the newly generated color scheme is displayed below.\n\n.. code-block:: console\n   \n   $ gecos --matrix BLOSUM62 --lmin 60 --lmax 75 -f awesome_colors.json\n\n.. image:: https://raw.githubusercontent.com/biotite-dev/gecos/master/doc/static/assets/figures/main_example_alignment.png\n\nInstallation\n============\n\nIn order to use *Gecos* you need to have Python (at least 3.6) installed.\nFurthermore, the following Python packages are required:\n\n   - **biotite**\n   - **numpy**\n   - **matplotlib**\n   - **scikit-image**\n\nIf these prerequisites are met, *Gecos* is simply installed via\n\n.. code-block:: console\n\n   $ pip install gecos',
    'author': 'Patrick Kunzmann',
    'author_email': 'patrick.kunzm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gecos.biotite-python.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
